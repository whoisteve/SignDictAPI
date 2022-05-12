from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import urllib.request
import pandas as pd
import sys
import csv

csv.field_size_limit(sys.maxsize)

def extractWord():
    # https://wortschatz.uni-leipzig.de/de/download
    df = pd.read_csv('input/deu_mixed-typical_2011_10K-words.txt', sep='\t', engine='python', encoding='utf-8', error_bad_lines=False, header=None)
    print(df)

def querySignDict(word):
    queryWord = word

    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(url="https://signdict.org/graphql-api/graphiql")

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Provide a GraphQL query
    query = gql(
        """
        {
          search(word: "%s") {
            id
            text
            type
            currentVideo {
              videoUrl
              license
              copyright
              originalHref
              user {
                name
              }
            }
          }
        }
    """%word
    )

    # Execute the query on the transport
    result = client.execute(query)
    print(result)

def downloadVideo(url, fileName):
    urllib.request.urlretrieve(url, fileName + ".mp4")
    print()

if __name__ == '__main__':
    extractWord()
    querySignDict("Zug")
