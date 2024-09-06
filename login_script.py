import json
import asyncio
from pyppeteer import launch
from datetime import datetime, timedelta
import aiofiles
import random
import requests
import os

# 从环境变量中获取 NOTIFYME Token
NOTIFYME_TOKEN = os.getenv('NOTIFYME_TOKEN')

def format_to_iso(date):
    return date.strftime('%Y-%m-%d %H:%M:%S')

async def delay_time(ms):
    await asyncio.sleep(ms / 1000)

# 全局浏览器实例
browser = None

# telegram消息
message = ''

async def login(username, password, panel):
    global browser

    page = None  # 确保 page 在任何情况下都被定义
    serviceName = 'ct8' if 'ct8' in panel else 'serv00'
    try:
        if not browser:
            browser = await launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])

        page = await browser.newPage()
        url = f'https://{panel}/login/?next=/'
        await page.goto(url)

        username_input = await page.querySelector('#id_username')
        if username_input:
            await page.evaluate('''(input) => input.value = ""''', username_input)

        await page.type('#id_username', username)
        await page.type('#id_password', password)

        login_button = await page.querySelector('#submit')
        if login_button:
            await login_button.click()
        else:
            raise Exception('无法找到登录按钮')

        await page.waitForNavigation()

        is_logged_in = await page.evaluate('''() => {
            const logoutButton = document.querySelector('a[href="/logout/"]');
            return logoutButton !== null;
        }''')

        return is_logged_in

    except Exception as e:
        print(f'{serviceName}账号 {username} 登录时出现错误: {e}')
        return False

    finally:
        if page:
            await page.close()

async def main():
    global message
	#message = ''

    try:
        async with aiofiles.open('accounts.json', mode='r', encoding='utf-8') as f:
            accounts_json = await f.read()
        accounts = json.loads(accounts_json)
    except Exception as e:
        print(f'读取 accounts.json 文件时出错: {e}')
        message = f'读取 accounts.json 文件时出错: {e}'
        await send_notifyme_message(message)
        return

    for account in accounts:
        username = account['username']
        password = account['password']
        panel = account['panel']

        serviceName = 'ct8' if 'ct8' in panel else 'serv00'
        is_logged_in = await login(username, password, panel)

        if is_logged_in:
            now_utc = format_to_iso(datetime.utcnow())
            now_beijing = format_to_iso(datetime.utcnow() + timedelta(hours=8))
            #success_message = f'{serviceName}账号 {username} 于北京时间 {now_beijing}（UTC时间 {now_utc}）登录成功！'
            success_message = f'{username}_{serviceName}登录成功！ {now_beijing}'
            message += success_message + '\n'
            print(success_message)
        else:
            message += f'{username}_{serviceName}登录失败，请检查账号和密码。\n'
            print(f'{serviceName}账号 {username} 登录失败，请检查{serviceName}账号和密码是否正确。')

        delay = random.randint(1000, 8000)
        await delay_time(delay)
        
    #message += f'所有{serviceName}账号登录完成！'
    await send_notifyme_message(message)
    print(f'所有{serviceName}账号登录完成！')

async def send_notifyme_message(message):
    url = f"https://send.notifyme-f7507.521933.xyz"
    payload = {
		"data": {
			"to": NOTIFYME_TOKEN,
			"ttl": 86400,
			"priority": "normal",
			"data": {
				"title": "处理完成",
				"body": message,
				"group": "serv00",
				"bigText": True,
				"iconType": 9,
				"smallIcon":{
					"bitmap": "iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAACxMAAAsTAQCanBgAAAS4SURBVGhD7ZrJaxRBFMaTQUIIKiISVIIbKiFEERWJ+4JBI1EkiAcPHgXFg+DNi95c/gMPXhQVD6LiiiASN9wVEY0kJCIo6sVo3NHE31fzDFM9S7qTmbEH/ODjVVVX1Xuvu7rmvZouLxskent7RyJqYT2cAifDsbAajoK6XlFeXl7Z19fXS/kn/AW7je/hW9hFnw76tCGfwK+0RUZoR1BUBZspLoWLYB1Kh+lavmAOP4U34FV4OZFIfEIODUycgOu5+yfhN8pFhXTCM3Ad1cHdNAZvhM+TU/57YEu7bDLzBgZjxjDgfHJ4/CDb4Ggztx/eO0K/4fAma3+mNcUS2PgQGxenbgwJkw502BV3JwRsnI2te6zq4DkC1posBTSZdAg6MtxkKcCzNehIyeK/I3FD0BHFQqUCz9agIw9NlgIem3QI/iDWwgfs01XWFEtg42fEfAJKBZgO3hPBgTZEEx0VYscSsg07m1KdyApimRp4gkGxAfb8hsfheDMzPBg/i4GHYE9yuuID3V/MhvChE513MLbSqv2grYprLfAIfO00FBDoeGe6NlJNizZoq+TaDqs6eC87F7sQ2tZ2sg7PQWVsHphE71UNUlmi0twZcJJI/0ghDnMoen0JO+ALqF3zPutf9TRIN2yhuB/SLaH02iHNEYyRURr0BHGQ+jGoHHtAMF55usvZGTOKOZTVKW+XAd8pK29X6tpN21uo3WdAMFbpxWaKWxmjm6e2l6mOeJAjdPBAm0s3KW6BzsliAF1TpBPdp2QDZQ+y1bo6ZH0i2cAcrxB34SP4mP6dyE6k7nZkMF8FlE6dyIhzYAPzTUBmBWO8JxLZkUzQDUL8Pd6R1PL5CPW+yUFd1yZSAUdALcExUMdHY9EZOeYriCP/AkFHIt+JuOK/I3FD0JGhH08WD56tQUdOmow92JROWdHB27XYCXRQfYVODdYUS2DjDWxshIoWHLwnwgXFPqvoeDjZEj9gm0KmplQncoLflGb4gIGxALbcg6vNvNygvxfCU1ewt4gJjsIPmrCYQGcPPEJxmZnUD9oUJWQGg1rhGqt6YKBygBXwALwOv0hZPqE5NTfFfXAlTMuNBF2jX6tVHTKGKHQ8TXUvIYCCw4ygzzA4nWId1F9vCvLGQcVPiqXcX29GvYteGA8Vl72DykcUdD5DdiCzHklh31zEbvo0ozt8GE/9DtwOo+fJeQK6q+E2eM/McqAePYzXOMQteJXr15C3kaGSoqjAhpHMPQ+dS6guhwuop0UgXB969GuOKR1VFtnOGLc8aNdRjcL4z8iMjtJHv1X611dhvJ50DdTSnAaV/U1l7ID/F+bFkTBAkdZ6Wj7C/Gl3dzAIOpKXSTNBdxVWQi0V5fAqF0xfwSYuNoKOFOQFLhA8W4OOXDRZCjhr0sF72XmBdH7UylqebU2xBDbqm5WFsP+peE/ELjTS8VyyJX7AtguI5alOZAWdE2zFG2DcPuHYZCZGA+PlkMJ5fdjyIzll8YBOBZH6oEcf1eTcYb13JBeYSGe5Kyk2wgWwlsdbqM+cFA4pU70UagmB0I4EgVJtDPUo0t91ioInQh1gi/roJdeHZ4qA30CFMwr+dOyqF1gfn4Uy3EdZ2R9iRT/rEFJ9JgAAAABJRU5ErkJggg==",
					"color": "#007ec150"
				}
			}
		}
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            print(f"发送消息到NotifyMe失败: {response.text}")
    except Exception as e:
        print(f"发送消息到NotifyMe时出错: {e}")

if __name__ == '__main__':
    asyncio.run(main())
