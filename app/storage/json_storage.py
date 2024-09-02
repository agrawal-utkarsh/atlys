import json
import os
from typing import List, Dict
from .storage import StorageBase
from ..models import Product, ScrapedData

class JSONStorage(StorageBase):
    def __init__(self, filename: str):
        self.filename = filename

    def save(self, data: List[Product]):
        validated_data = ScrapedData(products=data)
        with open(self.filename, 'w') as file:
            json.dump(validated_data.dict()["products"], file, indent=4)

    def load(self) -> List[Dict]:
        try:
            with open(self.file_path, 'r') as file:
                data = file.read().strip()
                if not data:
                    return []  # Return an empty list if the file is empty
                return json.loads(data)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return []  # Return an empty list in case of JSON decode error
        except FileNotFoundError:
            return []  # Return an empty list if the file is not found
        except Exception as e:
            print(f"Unexpected error: {e}")
            return []  # Return an empty list in case of other errors


    def update_data(self, new_data: List[Product]) -> int:
        current_data = self.load()
        updated_data = []
        for new_item in new_data:
            for current_item in current_data:
                if current_item.product_title == new_item.product_title:
                    if current_item.product_price != new_item.product_price:
                        updated_data.append(new_item)
                    break
            else:
                updated_data.append(new_item)
        self.save(updated_data)
        return len(updated_data)
