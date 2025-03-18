import requests

# GitHub Unfollow Bot
# Bu script, GitHub'da seni takip etmeyenleri otomatik olarak takipten çıkarır.

# GitHub API Token (Bunu .env dosyasından veya güvenli bir yerden alabilirsin)
GITHUB_TOKEN = "your_github_token_here"
USERNAME = "your_github_username_here"

# API isteği için başlıklar
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}


def get_all_users(url):
    users = []
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            users.extend(user['login'] for user in response.json())
            # Sayfalama için 'Link' başlığını kontrol et
            url = response.links.get('next', {}).get('url')
        else:
            print(f"{url} isteği başarısız oldu.")
            break
    return users


def get_following():
    url = f"https://api.github.com/users/{USERNAME}/following?per_page=100"
    return get_all_users(url)


def get_followers():
    url = f"https://api.github.com/users/{USERNAME}/followers?per_page=100"
    return get_all_users(url)


def unfollow_user(username):
    url = f"https://api.github.com/user/following/{username}"
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print(f"{username} takipten çıkarıldı.")
    else:
        print(f"{username} takipten çıkarılamadı: {response.status_code}")


def find_and_unfollow_non_followers():
    following = set(get_following())
    followers = set(get_followers())
    non_followers = following - followers

    if non_followers:
        print("Seni takip etmeyen takip ettiklerin takipten çıkarılıyor...")
        for user in non_followers:
            unfollow_user(user)
    else:
        print("Tüm takip ettiklerin seni de takip ediyor!")


if __name__ == "__main__":
    find_and_unfollow_non_followers()
