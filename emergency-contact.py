import requests
from getpass import getpass
from requests.auth import HTTPBasicAuth

dnac_domain = 'https://sandboxdnac2.cisco.com'
print('===================================')
print('Welcome to the DevNet Sandbox Demo!')
print('===================================')

url = '{0}/dna/system/api/v1/auth/token'.format(dnac_domain)

print('first, we need to get an auth token by making a request to \n{0}\n'.format(url))
print('use the credentials from the sandbox portal\n')

username = input('username: ')
password = getpass(prompt='password for {0}: '.format(username))

auth = HTTPBasicAuth(username=username, password=password)

input('press ENTER to request your auth token')

token = requests.post(url=url, auth=auth)

try: 
    data = token.json()
    t = data['Token']
    print('your token is: \n\n{0}'.format(t))
except:
    print('error requesting token: {0}'.format(token.text))
    print('please restart the script to try again!')
    exit()

print('===================================')
print('Great! now that we have an auth token, we make a request against the endpoint')
end = input('What endpoint would you like to query? (note: include leading /): ')

url = '{0}{1}'.format(dnac_domain,end)

headers = {
    'X-Auth-Token':t,
    'Content-Type': 'application/json'
}
input('press ENTER to make an API call to {0}'.format(url))
resp = requests.get(url=url, headers=headers)

try:
    count = resp.json()
except:
    count = -1

while resp.status_code != 200 or count == -1:
    print('Uh-oh! Something went wrong with that input. Please check your spelling and try again')
    end = input('What endpoint would you like to query? (note: include leading /): ')
    url = '{0}{1}'.format(dnac_domain,end)
    input('press ENTER to make an API call to {0}'.format(url))
    resp = requests.get(url=url, headers=headers)
    try:
        count = resp.json()
    except:
        count = -1

print(resp.text)