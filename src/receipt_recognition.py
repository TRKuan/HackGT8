import os

from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

def analyse_receipt(receipt):
  endpoint = os.environ['FORM_RECOGNIZER_ENDPOINT']
  key = os.environ['FORM_RECOGNIZER_SUBSCRIPTION_KEY']
  document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
  )

  poller = document_analysis_client.begin_analyze_document('prebuilt-receipt', receipt, locale='en-us')
  receipts = poller.result()
  if len(receipts.documents) > 0:
    return receipts.documents[0]

def get_items(receipt):
  receipt = analyse_receipt(receipt)
  if receipt is None:
    return []
  
  
  items = receipt.fields.get('Items')
  if items is None:
    return []
  
  item_info_list = []
  for idx, item in enumerate(items.value):
    item_info = {}
    item_name = item.value.get('Name')
    item_total_price = item.value.get("TotalPrice")
    if item_name is None or item_total_price is None:
      continue
    if item_name.confidence < 0.9 or item_total_price.confidence < 0.9:
      continue

    item_info['item_name'] = item_name.value
    item_info['price'] = item_total_price.value
    
    item_quantity = item.value.get("Quantity")
    if item_quantity and item_quantity.confidence > 0.9:
      item_info['count'] = item_quantity.value
    
    merchant_name = receipt.fields.get('MerchantName')
    if merchant_name:
      item_info['store_name'] = merchant_name.value
    
    transaction_date = receipt.fields.get('TransactionDate')
    if transaction_date:
      item_info['date'] = transaction_date.value
    
    item_info_list.append(item_info)
  
  return item_info_list