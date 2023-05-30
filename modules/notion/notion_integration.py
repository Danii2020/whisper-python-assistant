import notion_client
import dotenv
import os

dotenv.load_dotenv()

notion = notion_client.Client(auth=os.getenv("NOTION_API_KEY"))
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

class Notion:
    def create_page(self, properties, children, db_id=NOTION_DATABASE_ID):
        notion_page = notion.pages.create(
            parent={"database_id":db_id},
            properties=properties,
            children=children
        )
        return notion_page