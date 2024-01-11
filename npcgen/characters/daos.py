from sqlalchemy import text

from ..core.db_utils import create_record, read_record_by_attr, record_exists
from .models import Character, Item, Skill


class CharacterDao:
    def __init__(self, session):
        self.session = session

    def create_character(self, character):
        character_dict = self._character_to_dict(character)
        character_id = create_record(
            self.session, "character", "id", **character_dict
        )[0]

        if character.items:
            for item in character.items:
                self.add_item_to_character(
                    character_id, item.id, item.proficiency
                )

        if character.skills:
            for skill in character.skills:
                self.add_skill_to_character(
                    character_id, skill.id, skill.proficiency
                )

        self.session.commit()
        return character_id

    def character_with_name_exists(self, name):
        return record_exists(self.session, "character", "name", name)

    def add_item_to_character(self, character_id, item_id, proficiency):
        create_record(
            self.session,
            "character_item",
            character_id=character_id,
            item_id=item_id,
            proficiency=proficiency,
        )
        self.session.commit()

    def add_skill_to_character(self, character_id, skill_id, proficiency):
        create_record(
            self.session,
            "character_skill",
            character_id=character_id,
            skill_id=skill_id,
            proficiency=proficiency,
        )
        self.session.commit()

    def _character_to_dict(self, character):
        return {
            "user_id": character.user_id,
            "name": character.name,
            "race_id": character.race_id,
            "class_id": character.class_id,
            "alignment_id": character.alignment_id,
            "hints": character.hints,
            "backstory": character.backstory,
            "plot_hook": character.plot_hook,
            "template_id": character.template_id,
            "level": character.level,
            "gender": character.gender,
            "strength": character.strength,
            "dexterity": character.dexterity,
            "constitution": character.constitution,
            "intelligence": character.intelligence,
            "wisdom": character.wisdom,
            "charisma": character.charisma,
            "perception": character.perception,
            "armor_class": character.armor_class,
            "hit_points": character.hit_points,
            "speed": character.speed,
            "fortitude_save": character.fortitude_save,
            "reflex_save": character.reflex_save,
            "will_save": character.will_save,
            "is_template": character.is_template,
        }

    def _map_record_to_character(self, record):
        return Character(
            user_id=record.user_id,
            name=record.name,
            race_id=record.race_id,
            race_name=record.race_name,
            class_id=record.class_id,
            class_name=record.class_name,
            alignment_id=record.alignment_id,
            alignment_name=record.alignment_name,
            hints=record.hints,
            backstory=record.backstory,
            plot_hook=record.plot_hook,
            template_id=record.template_id,
            template_name=record.template_name,
            level=record.level,
            gender=record.gender,
            strength=record.strength,
            dexterity=record.dexterity,
            constitution=record.constitution,
            intelligence=record.intelligence,
            wisdom=record.wisdom,
            charisma=record.charisma,
            perception=record.perception,
            armor_class=record.armor_class,
            hit_points=record.hit_points,
            speed=record.speed,
            fortitude_save=record.fortitude_save,
            reflex_save=record.reflex_save,
            will_save=record.will_save,
            id=record.id,
            is_template=record.is_template,
        )


class ItemDao:
    def __init__(self, session):
        self.session = session

    def get_item_by_properties(self, **kwargs):
        query = self.session.execute(
            text(
                """
            SELECT * FROM item
            WHERE name = :name
            AND damage = :damage
            AND damage_type = :damage_type
            AND item_type = :item_type
            """
            ),
            kwargs,
        )
        record = query.fetchone()
        return self._map_record_to_item(record) if record else None

    def create_item(self, item):
        item_dict = self._map_item_to_dict(item)
        record = create_record(self.session, "item", "id", **item_dict)
        self.session.commit()
        return record[0]

    def _map_item_to_dict(self, item):
        return {
            "name": item.name,
            "item_type": item.item_type,
            "damage": item.damage,
            "damage_type": item.damage_type,
            "traits": item.traits,
        }

    def _map_record_to_item(self, record):
        return Item(
            id=record.id,
            name=record.name,
            item_type=record.item_type,
            damage=record.damage,
            damage_type=record.damage_type,
            traits=record.traits,
        )


class SkillDao:
    def __init__(self, session):
        self.session = session

    def get_skill_by_name(self, name):
        record = read_record_by_attr(self.session, "skill", "name", name)
        return self._map_record_to_skill(record) if record else None

    def create_skill(self, skill):
        skill_dict = self._map_skill_to_dict(skill)
        record = create_record(self.session, "skill", "id", **skill_dict)
        self.session.commit()
        return record[0]

    def _map_skill_to_dict(self, skill):
        return {
            "name": skill.name,
            "description": skill.description,
        }

    def _map_record_to_skill(self, record):
        return Skill(
            id=record.id,
            name=record.name,
            description=record.description,
        )
