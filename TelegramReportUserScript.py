"""
====================================
    趋于飞机批量举报工具 v1.0.0    
====================================

✨ 功能简介
----------
一个强大的 Telegram 用户举报自动化工具

📱 Telegram社群信息
----------
• 官方频道：@QUYUkjpd
• 交流群组：@QUYUkjq
• 联系作者：@Lawofforce

💝 赞助支持
----------
感谢您的支持，这是我们持续改进的动力！

• TRC20-USDT 钱包地址:
  TQ2gs6167orQSVWVNHWrKq9SZ8a5WRETZs

⚠️ 免责声明
----------
• 本工具仅供学习交流使用
• 严禁用于非法用途
• 使用本工具所产生的一切后果由使用者自行承担

📜 许可协议
----------
MIT License
Copyright (c) 2024 All Rights Reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
"""

import asyncio
import os
import shutil

from telethon import TelegramClient
from telethon.tl.functions.account import ReportPeerRequest
from telethon.tl.types import *
from telethon.tl.types import User

sen_dir = "sessions"
reportReasons = ["虐待儿童", "版权问题", "虚假消息", "非法药物", "其他问题", "非法人员", "非法组织", "垃圾邮件",
                 "暴力行为"]


async def main():
    report_user = input("请输入要举报的用户名或ID:")
    report_count = int(
        input("请输入要举报的次数(可用账号数少于输入次数时将重复举报, 输入0时可用账号数有多少个就举报多少次):"))
    for x in range(len(reportReasons)):
        print(f"{x+1}:{reportReasons[x]}")
    report_type = input("请选择举报原因：")
    if report_type == "1":
        report_type = InputReportReasonChildAbuse()
    elif report_type == "2":
        report_type = InputReportReasonCopyright()
    elif report_type == "3":
        report_type = InputReportReasonFake()
    elif report_type == "4":
        report_type = InputReportReasonIllegalDrugs()
    elif report_type == "5":
        report_type = InputReportReasonOther()
    elif report_type == "6":
        report_type = InputReportReasonPersonalDetails()
    elif report_type == "7":
        report_type = InputReportReasonPornography()
    elif report_type == "8":
        report_type = InputReportReasonSpam()
    elif report_type == "9":
        report_type = InputReportReasonViolence()
    print(report_type)
    report_msg = input("请输入举报内容：")
    count = 0
    # target_user = None
    exit_flag = False
    while not exit_flag:
        for file in os.listdir(sen_dir):
            base_name, ext = os.path.splitext(file)
            is_dir = os.path.isdir(os.path.join(sen_dir + "/" + base_name))
            if count == report_count and report_count != 0:
                print(f"举报结束, 累计举报次数：{count}次, 已完成指定举报任务数")
                exit_flag = True
                break
            if ext == ".session" or is_dir:
                s_dir = sen_dir + "/" + base_name + ".session"
                if is_dir:
                    s_dir = sen_dir + "/" + base_name + "/" + base_name + ".session"
                client = TelegramClient(s_dir, 2040,
                                        "b18441a1ff607e10a989891a5462e627")
                await client.connect()
                try:
                    if await client.is_user_authorized() is False:
                        print("账号不可用：" + base_name + "已请求删除此账号文件夹")
                        await client.disconnect()
                        shutil.rmtree(sen_dir + "/" + base_name)
                        continue
                    # if target_user is None:
                    target_user = await client.get_entity(report_user)
                    while isinstance(target_user, User) is False:
                        report_user = input(
                            "输入的用户名或ID (" + report_user + ") 不是一个正确的用户, 请重新输入要举报的用户名或ID:")
                        target_user = await client.get_entity(report_user)
                    target_peer = InputPeerUser(target_user.id, target_user.access_hash)
                    report_result = await client(ReportPeerRequest(
                        peer=target_peer,
                        reason=report_type,
                        message=report_msg
                    ))
                    if report_result is True:
                        count += 1
                        if report_count == 0:
                            print(f"账号 {base_name} 已对 {report_user} 进行举报, 当前举报次数：{count}次")
                        else:
                            print(
                                f"账号 {base_name} 已对 {report_user} 进行举报, 当前举报次数：{count}次, 需举报{report_count}次, "
                                f"还剩{(report_count - count)}次")
                    else:
                        print(f"账号 {base_name} 对 {report_user} 举报失败!!!")
                    await client.disconnect()
                except Exception as e:
                    print(f"{base_name} 举报出现异常：{str(e)}")
                    await client.disconnect()

        if report_count == 0:
            print(f"举报结束, 累计举报次数：{count}次, 本次举报次数为按可用账号数量进行举报")
            break


asyncio.run(main())
