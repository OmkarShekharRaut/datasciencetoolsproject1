import pandas as pd
from sklearn.linear_model import LinearRegression

df=pd.read_csv("users.csv")

r_df=pd.read_csv("repositories.csv")

#top 5 users with highest no. of followers
top_users=df.sort_values(by='followers',ascending=False).head(5)
print(top_users['login'])
print(top_users['followers'])

print('')

#5 earliest registration
ear_reg=df.sort_values(by='created_at',ascending=True).head(5)
print(ear_reg['login'])

print('')

#top 3 license names
without_na=r_df[r_df['license_name']!='']
top_license=without_na['license_name'].value_counts().head(3)
print(top_license)

print('')

#top company
top_com=df['company'].value_counts().idxmax()
print(top_com)

print('')

#top language
unique_user_lang=r_df[['login','language']].drop_duplicates()
top_lang=unique_user_lang['language'].value_counts().idxmax()
print(top_lang)

print('')

#second higest lang for users after 2020
user_2020=df[df['created_at']>'2020-12-31']
no_dup=unique_user_lang[unique_user_lang['login'].isin(user_2020['login'])]
sec_top_lang=no_dup['language'].value_counts().index[1]
print(sec_top_lang)

print('')

#highest avg stars for language
high_avg_stars=r_df.groupby('language')['stargazers_count'].mean().idxmax()
print(high_avg_stars)

print('')

#top 5 leader strength (followers/(1+following))
df2=df.copy()
df2['leader']=df2['followers']/(df2['following']+1)
top_leaders=df2.sort_values(by='leader',ascending=False).head(5)
print(top_leaders['login'])

print('')

#correlation between followers and repositories
correlation=df['followers'].corr(df['public_repos'])
print(f"{correlation:.3f}")

print('')

#Linear regression between followers and repos
X=df[['public_repos']]
y=df['followers']
LR=LinearRegression()
LR.fit(X,y)
coef=LR.coef_[0]
print(f"{coef:.3f}")

print('')

#correlation between has_projects and has_wiki
r_df['has_projects']=r_df['has_projects'].fillna(False)
r_df['has_wiki']=r_df['has_wiki'].fillna(False)
corr_pro_wiki=r_df['has_wiki'].corr(r_df['has_projects'])
print(f"{corr_pro_wiki:.3f}")

print('')

#following of hireable and not
df['hireable']=df['hireable'].fillna(False).astype(bool)
df['following']=df['following'].fillna(0)
avg_hireable=df[df['hireable']]['following'].mean()
avg_nh=df[~df['hireable']]['following'].mean()
print(f"{(avg_hireable-avg_nh):.3f}")

print('')

#bios and followers relation
df3=df.copy()
df3['bio_len']=df3['bio'].fillna('').apply(lambda x:len(x.split()))
X=df3[['bio_len']]
y=df3['followers']
LR.fit(X,y)
coef2=LR.coef_[0]
print(f"{coef2:.3f}")

print('')

#top 5 repo creators on weekend
r_df['created_at']=pd.to_datetime(r_df['created_at'],utc=True)
weekend_repos = r_df[r_df['created_at'].dt.weekday >= 5]
top_wkd_repo=weekend_repos['login'].value_counts().head(5)
print(top_wkd_repo)

print('')

#relation between hireable and email
df['email']=df['email'].fillna('')
h_total=len(df[df['hireable']])
h_with_email=len(df[(df['hireable'])&(df['email']!='')])
x=h_with_email/h_total
nh_total=len(df[~df['hireable']])
nh_with_email=len(df[(~df['hireable'])&(df['email']!='')])
y=nh_with_email/nh_total
print(f"{(x-y):.3f}")

print('')

#most common surname
df=df.dropna(subset=['name'])
df['name']=df['name'].str.strip()
df['surname']=df['name'].apply(lambda x: x.split()[-1] if (len(x.split())>1) else None)
print(f"{df['name']},{df['surname']}")
top_surname=df['surname'].dropna().value_counts()
most_common_surnames=top_surname[top_surname==top_surname.max()].index.tolist()
print(most_common_surnames)
