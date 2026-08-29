from qdrant_client.models import PayloadSchemaType
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    MatchValue,
    Filter,
    FieldCondition
)
from numpy import array
from app.utils import QuadrentVectorException
from app.config import secret_manager
from uuid import uuid4
import logfire
from typing import List


class QdrentVector:
    def __init__(self):

       # connect to Qdrant Cloud
        self.qdrent_client = QdrantClient(
            url=secret_manager.qdrent_endpoint,
            api_key=secret_manager.qdrent_api
        )

        if self.qdrent_client.collection_exists is not True:
            self.qdrent_client.recreate_collection(
                collection_name=secret_manager.qdrent_collection_name,
                vectors_config=VectorParams(
                    size=self.qdrent_client.get_embedding_size(
                        model_name=secret_manager.Embedding_model
                    ),
                    distance=Distance.COSINE
                )
            )
            logfire.info("qdrent collection created in cluster already")

            self.qdrent_client.create_payload_index(
                collection_name=secret_manager.qdrent_collection_name,
                field_name="user_id",
                field_schema=PayloadSchemaType.KEYWORD,
            )

            self.qdrent_client.create_payload_index(
                collection_name=secret_manager.qdrent_collection_name,
                field_name="session_id",
                field_schema=PayloadSchemaType.KEYWORD,
            )
        else:
            logfire.info(
                f"qudrent collenction name {secret_manager.qdrent_collection_name} this qdrent cluster already exists, skipping creation.")

    def upload_data(self, user_id: str, user_text: str, vector: List[array], session_id: str) -> dict[dict, str]:
        try:
            opration_respones = self.qdrent_client.upsert(
                collection_name=secret_manager.qdrent_collection_name,
                points=[
                    PointStruct(
                        id=str(uuid4()),
                        vector=vector,
                        payload={
                            "user_id": user_id,
                            "session_id": session_id,
                            "text": user_text
                        }
                    )
                ],
                timeout=60
            )
            logfire.warning(
                f"this is the session id:{session_id} of the upload db method")

            logfire.info("Data uploaded to Qdrent collection successfully.")
            return opration_respones, session_id
        except Exception as error:
            logfire.error(f"Error uploading data to Qdrent: {error}")
            raise QuadrentVectorException(
                "vectorization failed for this time please try again later")

    def delete_vectors(self, user_id: str, session_id: str):
        try:
            opration_respones = self.qdrent_client.delete(
                collection_name=secret_manager.qdrent_collection_name,
                points_selector=Filter(
                    must=[
                        FieldCondition(
                            key="user_id",
                            match=MatchValue(
                                value=user_id
                            )
                        ),
                        FieldCondition(
                            key="session_id",
                            match=MatchValue(
                                value=session_id
                            )
                        )
                    ]
                ),
                timeout=60
            )
            logfire.info("All data points deleted from Qdrent collection.")
            return opration_respones
        except Exception as error:
            logfire.error(f"Error deleting data points from Qdrent: {error}")
            raise QuadrentVectorException(
                "Failed to delete data points from Qdrent. Please try again later.")
        finally:
            self.qdrent_client.close()
