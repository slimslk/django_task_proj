from typing import Any


def prepare_instance_to_update(update_data: dict, instance: Any, fields_name_list: list[str]) -> tuple[Any, list[str]]:
    update_fields: list[str] = []
    for field in fields_name_list:
        if field in update_data:
            data = update_data.get(field)
            if data != getattr(instance, field):
                setattr(instance, field, data)
                update_fields.append(field)
    return instance, update_fields
