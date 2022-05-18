# coding:utf-8
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

############################################
##
##　クロネコビッグデータ基盤　共通処理
##
############################################

# ストレージ'(kbd2datalake003)
GEN2_CON_STR = 'DefaultEndpointsProtocol=https;AccountName=kbd2eadatalake003;AccountKey=pSKmnhb7+JxPXZ6wVPtzVNOiYy9Qs+puTrPgXhYvbGxBhkxSy/79gFKgmyTxi2aBO+GDbhkykvWRloEb7aIU0Q==;EndpointSuffix=core.windows.net'
GEN2_ACCOUNT_NAME = 'kbd2eadatalake003'
GEN2_ACCOUNT_KEY = 'pSKmnhb7+JxPXZ6wVPtzVNOiYy9Qs+puTrPgXhYvbGxBhkxSy/79gFKgmyTxi2aBO+GDbhkykvWRloEb7aIU0Q=='

def get_kbd_gen2_con_str():
    """
    KBDのストレージ接続文字列を取得します。
        
    Returns
    ----------
    con_str : str
        KBD2ストレージ接続文字列
    """
    con_str = GEN2_CON_STR
    return con_str

def get_blob_service_client(con_str):
    """
    ブロブサービスクライアントを取得します。
    
    Parameters
    ----------
    con_str : str
        ストレージクライアント接続文字列
    
    Returns
    ----------
    blob_service_client : BlobServiceClient
        ブロブサービスクライアント
    """
    blob_service_client = BlobServiceClient.from_connection_string(con_str)
    return blob_service_client

def get_container_client(con_str, container_name):
    """
    コンテナークライアントを取得します。
    
    Parameters
    ----------
    con_str : str
        ストレージ接続文字列
    container_name : str
        コンテナ名
    
    Returns
    ----------
    container_client : ContainerClient
        コンテナークライアント
    """
    blob_service_client=get_blob_service_client(con_str)
    container_client = blob_service_client.get_container_client(container_name)
    return container_client

def get_kbd_container_client(container_name):
    """
    コンテナークライアントを取得します。
    
    Returns
    ----------
    kbd_container_client : ContainerClient
        KBD用のコンテナークライアント
    """
    kbd_container_client = get_container_client(get_kbd_gen2_con_str(), container_name)
    return kbd_container_client

def get_kbd_blob_service_client():
    """
    KBD用のブロブサービスクライアントを取得します。

    Returns
    ----------
    kbd_blob_service_client : BlobServiceClient
        KBD用のブロブサービスクライアント
    """
    kbd_blob_service_client = get_blob_service_client(get_kbd_gen2_con_str())
    return kbd_blob_service_client

def get_blob_list_search(container_client,name_starts_with):
    """
    ブロブ一覧を取得します。
    
    Parameters
    ----------
    container_client : ContainerClient
        コンテナークライアント
    
    Returns
    ----------
    blob_list : list
        ブログファイル一覧
    """
    blob_list = container_client.list_blobs(name_starts_with=name_starts_with)
    return blob_list

def get_kbd_blob_list_search(container_name, name_starts_with):
    """
    KBD用ブロブ一覧を取得します。

    Parameters
    ----------
    name_starts_with : name_starts_with
        検索対象のファイルパス
        
    Returns
    ----------
    kbd_blob_list : list
        ブログファイル一覧
    """
    kbd_blob_list = get_blob_list_search(get_kbd_container_client(container_name),name_starts_with)

    blobList=[]
    for blob in kbd_blob_list:
        # DDS/KKKSフォルダ配下・KKKSフォルダ配下は機微情報のため検索対象除外
        if 'DDS/KKKS/' in blob.name or 'KKKS/KBDKKS' in blob.name:
            continue
        if name_starts_with in blob.name:
            # リストに要素追加
            blobList+=[blob.name]
    return blobList

def download_blob(blob_service_client, container_name, blob_file_name, download_file_path):
    """
    ストレージからブロブをダウンロードします。
    
    Parameters
    ----------
    blob_service_client blob_service_client
        ブロブサービスクライアント
    container_name
        コンテナ名
    blob_file_name
        ダウンロード先のブロブファイル名
    download_file_path
        ダウンロードファイルパス
    """
    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_file_name)
    with open(download_file_path, "wb") as download_file:
        download_file.write(blob_client.download_blob().readall())

def download_kbd_blob(container_name, blob_file_name, download_file_path):
    """
    KBD用ストレージからブロブをダウンロードします。
    
    Parameters
    ----------
    blob_file_name
        ダウンロード先のブロブファイル名
    download_file_path
        ダウンロードファイルパス
    """
    download_blob(get_kbd_blob_service_client(), container_name, blob_file_name, download_file_path)
