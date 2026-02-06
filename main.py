"""Основной модуль программы"""

from api.wbapi import WbApi
from api.common import Common
from api.usr_manag import UserManager
from api.enums.user_privilege import UserPrivilege as Privilege

if __name__ == "__main__":

    wbapi = WbApi()
    # common = Common(wbapi=wbapi)
    usr_man = UserManager(wbapi=wbapi)
    # ping = common.ping()
    # news = common.get_news()
    # s_info = common.get_seller_info()

    # list_priv = []
    # for priv in Privilege:
    #     list_priv.append(priv.value)

    # result = usr_man.invite_user(
    #     list_priv=list_priv, phone="79628496792", position="Технический директор"
    # )

    u_list = usr_man.get_users_list()

    print("Done!")
