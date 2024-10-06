import chromadb
import pandas as pd
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
import openai
import os
from dotenv import load_dotenv

load_dotenv()

EMBEDDING_MODEL = 'text-embedding-3-small'
if os.getenv("OPENAI_API_KEY") is not None:
    openai_ef = OpenAIEmbeddingFunction(api_key=os.getenv("OPENAI_API_KEY"), model_name=EMBEDDING_MODEL)
else:
    print("OPENAI_API_KEY environment variable not found.")

class VectorizeData():

    def __init__(self) -> None:
        self.chroma_client = chromadb.PersistentClient("./data/chroma")
        self.collection = self.chroma_client.get_collection(name="PatientData", embedding_function=openai_ef)

    def vectorize_data(self):
        try:

            df = pd.read_csv('Synthetic_Data.csv')
            df.set_index('Patient_ID', inplace=True)
            columns=len(df.columns)

            documents = []
            metadatas = []
            ids =[]
            doc_data=[]
            id=1
            for index, row in df.iterrows():
                doc_data.append(index)
                for i in range(columns):
                    doc_data.append(str(row[i]))
                documents.append(' '.join(doc_data))
                metadatas.append({'item_id':index})
                ids.append(str(id))
                id+=1
                doc_data=[]

            self.collection.upsert(
                documents= documents,
                ids = ids
            )
            print("loaded data in chromadb")
        except Exception as e:
            print(f"Error while loading chromadb : {str(e)}")

    def fetch_data(self,input_query):
        #semantic search with chroma
        search_result=self.collection.query(
            query_texts=input_query,
            n_results=2,
            include=['documents']
        )
        print(search_result)
        # Extract and prepare context from search result
        context = []
        for obj in search_result["documents"]:
            context.append(obj)
        return context

if __name__ == "__main__":
    data_obj = VectorizeData()
    # data_obj.vectorize_data()
    question = input("Enter your query")
    print(data_obj.fetch_data(question))


