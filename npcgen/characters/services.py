import copy

from ..core.expections import ValidationError
from .models import Character, Item, Skill


class CharacterGeneratorService:
    def __init__(self, character_dao):
        self.character_dao = character_dao

    def generate_character(self, options, user_id=None):
        template = self.character_dao.get_character(
            options.get("template_id"),
            populate_items=True,
            populate_skills=True,
        )

        if template is None:
            raise ValidationError("template_id", "Template not found")

        character = copy.deepcopy(template)
        character.id = None
        character.is_template = False

        character.user_id = user_id
        character.template_id = options.get("template_id")
        character.alignment_id = options.get("alignment_id")
        character.class_id = options.get("class_id")
        character.race_id = options.get("race_id")
        character.hints = options.get("hints")

        character.apply_random_modifiers()

        created_id = self.character_dao.create_character(character)

        return created_id


class CharacterTemplateService:
    def __init__(self, character_dao, item_dao, skill_dao):
        self.character_dao = character_dao
        self.item_dao = item_dao
        self.skill_dao = skill_dao

    def create_template(self, character_data):
        template_exists = self.character_dao.character_with_name_exists(
            character_data["name"]
        )

        if template_exists:
            raise ValidationError(
                "name", "Template with this name already exists"
            )

        # Create character
        character = Character(
            name=character_data["name"],
            race_id=character_data["race_id"],
            alignment_id=character_data["alignment_id"],
            level=character_data["level"],
            strength=character_data["strength"],
            intelligence=character_data["intelligence"],
            dexterity=character_data["dexterity"],
            charisma=character_data["charisma"],
            constitution=character_data["constitution"],
            wisdom=character_data["wisdom"],
            armor_class=character_data["armor_class"],
            hit_points=character_data["hit_points"],
            speed=character_data["speed"],
            fortitude_save=character_data["fortitude_save"],
            reflex_save=character_data["reflex_save"],
            will_save=character_data["will_save"],
            perception=character_data["perception"],
            class_id=1,
            is_template=True,
        )

        character_id = self.character_dao.create_character(character)

        # Create or get items
        for item in character_data.get("items", []):
            existing_item = self.item_dao.get_item_by_properties(
                name=item["name"],
                damage=item["damage"],
                damage_type=item["damage_type"],
                item_type=item["item_type"],
                traits=item["traits"],
            )
            if existing_item:
                item_id = existing_item.id
            else:
                item_id = self.item_dao.create_item(
                    Item(
                        name=item["name"],
                        damage=item["damage"],
                        damage_type=item["damage_type"],
                        item_type=item["item_type"],
                        traits=item["traits"],
                    )
                )
            self.character_dao.add_item_to_character(
                character_id, item_id, item["proficiency"]
            )

        # Create or get skills
        for skill_data in character_data.get("skills", []):
            existing_skill = self.skill_dao.get_skill_by_name(
                name=skill_data["name"]
            )
            if existing_skill:
                skill_id = existing_skill.id
            else:
                skill_id = self.skill_dao.create_skill(
                    Skill(
                        name=skill_data["name"],
                        description=skill_data["note"],
                    )
                )

            self.character_dao.add_skill_to_character(
                character_id,
                skill_id,
                skill_data["proficiency"],
            )
