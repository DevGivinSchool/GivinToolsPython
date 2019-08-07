from bitrix24 import Bitrix24
import requests

clientId = "101"
clientCode = "local.5d2a0084b949b0.22675909"
clientSecret = "nJPDHkLog6QCJTpV7HMA4ZqvMTi63KU5HGbHckj955t0dFLN1S"
scope = 'user,crm'
domainName = "newhuman.bitrix24.ru"

def auth(bx24):
  auth_request = bx24.resolve_authorize_endpoint()

#####################################
  r = requests.get(auth_request)
  print(auth_request)
  data1 = r.url
  print(data1)
  print(r.content)

  exit(0)
#####################################

  # See https://github.com/yarbshk/pybitrix24
  auth_code = input("Enter auth code using URL: {}\n".format(auth_request))

  bx24.request_tokens(auth_code)
  tokens = bx24.get_tokens()
  print(tokens)

def get_deal_contacts(bx24):
  deals = []
  next = 0
  while True:
    deals_resp = bx24.call_method('crm.deal.list',
                                  {
                                      'filter': {
                                          # сделки ONLINE КЛУБ
                                          'CATEGORY_ID': 18,
                                          # Стадия сделки: оплатил
                                          # 'STAGE_ID': 'C18:PREPAYMENT_INVOICE'
                                          'STAGE_SEMANTIC_ID': "P"
                                       },
                                      'select': ["*"],
                                      'start': next
                                  })
    deals.extend(deals_resp['result'])
    if 'next' in deals_resp:
      next = deals_resp['next']
    else:
      break


  contact_ids = []
  for deal in deals:
    contact_ids.append(deal['CONTACT_ID'])

  contact_requests = {}
  for id in contact_ids:
    method_name = 'get_user_{}'.format(id)
    contact_requests[method_name] = ('crm.contact.get', {'ID': id})

  contacts = []
  next = 0
  batch_size = 50
  while True:
    batch = {key: contact_requests[key] for key in list(contact_requests)[next:next + batch_size]}
    contacts_resp = bx24.call_batch(batch)
    contacts_resp = contacts_resp['result']
    if contacts_resp['result']:
      contacts.extend(list(contacts_resp['result'].values()))
    else:
      break

    next += batch_size
    if next > len(contact_requests):
      break
    if contacts_resp['result_error']:
      print(contacts_resp['result_error'])
      break

  return contacts


if __name__ == '__main__':
  bx24 = Bitrix24(domainName, clientCode, clientSecret, scope=scope)

  auth(bx24)

  contacts = get_deal_contacts(bx24)

  print('{} contacts found'.format(len(contacts)))
  for contact in contacts:
    print(contact['LAST_NAME'],contact['NAME'])
  print('done')