import pandas as pd
import requests
import time

Token='my_token'
Headers={'Authorization':f'token {Token}'}

def fetch_users(location='Paris',min_followers=200):
    users=[]
    page=1
    while True:
        url=f"https://api.github.com/search/users?q=location:Paris+followers:>{min_followers}&per_page=30&page={page}"
        response=requests.get(url,headers=Headers)
        if response.status_code!=200:
            print("Error",response.json().get('message','unknown error'))
            break
        data=response.json().get('items',[])
        if not data:
            break
        users.extend(data)
        time.sleep(1)
        page+=1
        
    return users

def fetch_user_details(users):
    user_details=[]
    for user in users:
        url=f"https://api.github.com/users/{user['login']}"
        response=requests.get(url,headers=Headers)
        data=response.json()
        if response.status_code!=200:
            print("Error",data.get('message','unknown error'))
            break
        company=data.get('company','')
        if company:
            company=company.strip().lstrip('@').upper()
        user_details.append({'login':data.get('login',''),
                             'name':data.get('name',''),
                             'company':company,
                             'location':data.get('location',''),
                             'email':data.get('email',''),
                             'hireable':data.get('hireable',''),
                             'bio':data.get('bio',''),
                             'public_repos':data.get('public_repos',''),
                             'followers':data.get('followers',''),
                             'following':data.get('following',''),
                             'created_at':data.get('created_at','')})
        print(f'fetched details of {user['login']}')
        time.sleep(1)
    return user_details

def fetch_repos(username):
    repos=[]
    page=1
    MAX_PAGES=10
    while page<=MAX_PAGES:
        url=f"https://api.github.com/users/{username}/repos?per_page=50&page={page}"
        response=requests.get(url,headers=Headers)
        repo_data=response.json()
        if response.status_code!=200:
            print("Error",repo_data.get('message','unknown error'))
            break
        if not repo_data:
            break
        for data in repo_data:
            repos.append({'login':username,
                      'full_name':data.get('full_name',''),
                      'created_at':data.get('created_at',''),
                      'stargazers_count':data.get('stargazers_count',''),
                      'watchers_count':data.get('watchers_count',''),
                      'language':data.get('language',''),
                      'has_projects':data.get('has_projects',''),
                      'has_wiki':data.get('has_wiki',''),
                      'license_name': data.get('license')['name'] if data.get('license') else ''})
        print(f"got page {page} of user {username}")
        page+=1
        time.sleep(1)
    
    return repos

def create_csvfiles():
    users=fetch_users()
    user_details=fetch_user_details(users)
    users_df=pd.DataFrame(user_details)
    users_df.to_csv('users.csv',index=False)
    print('user.csv created')
    
    all_repos=[]
    for user in users:
        username=user['login']
        all_repos.extend(fetch_repos(username))
    repos_df=pd.DataFrame(all_repos)
    repos_df.to_csv('repositories.csv',index=False)
    print('repositories.csv created')
    
create_csvfiles()