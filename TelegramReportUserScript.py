"""
====================================
    趋于飞机批量举报工具 v1.0.1    
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

Copyright (c) 2025 git88848

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import asyncio
import os
import shutil
import time

from telethon import TelegramClient
from telethon.tl.functions.account import ReportPeerRequest
from telethon.tl.types import *
from telethon.tl.types import User

sen_dir = "sessions"

# 检查并创建sessions目录
if not os.path.exists(sen_dir):
    os.makedirs(sen_dir)
    print(f"已创建 {sen_dir} 目录，请将您的 Telegram 会话文件放入此目录")
    print("程序将在3秒后退出...")
    time.sleep(3)
    exit()

reportReasons = ["虐待儿童", "版权问题", "虚假消息", "非法药物", "其他问题", "非法人员", "非法组织", "垃圾邮件",
                 "暴力行为"]

async def get_user_input(prompt: str, timeout: int = 300) -> str:
    """异步获取用户输入，带超时处理"""
    print(prompt, end='', flush=True)
    try:
        return await asyncio.wait_for(
            asyncio.get_event_loop().run_in_executor(None, input),
            timeout=timeout
        )
    except asyncio.TimeoutError:
        print("\n输入超时，程序将退出...")
        raise

async def report_task(session_path, account_name, report_user, report_type, reason_text, report_msg, report_count):
    """单个举报任务的异步函数"""
    client = None
    try:
        client = TelegramClient(session_path, 2040, "b18441a1ff607e10a989891a5462e627")
        await client.connect()
        
        if not await client.is_user_authorized():
            print(f"账号不可用：{account_name} 已请求删除此账号文件夹")
            shutil.rmtree(os.path.dirname(session_path))
            return False
            
        target_user = await client.get_entity(report_user)
        if not isinstance(target_user, User):
            print(f"账号 {account_name}: 目标不是有效用户")
            return False
            
        target_peer = InputPeerUser(target_user.id, target_user.access_hash)
        report_result = await client(ReportPeerRequest(
            peer=target_peer,
            reason=report_type,
            message=report_msg
        ))
        
        if report_result is True:
            print(f"✅ 账号 {account_name} 成功举报用户 {report_user}")
            print(f"   举报原因: {reason_text}")
            print(f"   举报内容: {report_msg}")
            return True
        else:
            print(f"❌ 账号 {account_name} 举报失败 - 服务器返回失败")
            return False
            
    except Exception as e:
        print(f"❌ 账号 {account_name} 举报异常:")
        print(f"   错误信息: {str(e)}")
        return False
    finally:
        if client:
            await client.disconnect()

async def main():
    # 创建举报原因实例并显示中文说明
    report_type_map = {
        "1": (InputReportReasonChildAbuse(), "虐待儿童"),
        "2": (InputReportReasonCopyright(), "版权问题"),
        "3": (InputReportReasonFake(), "虚假消息"),
        "4": (InputReportReasonIllegalDrugs(), "非法药物"),
        "5": (InputReportReasonOther(), "其他问题"),
        "6": (InputReportReasonPersonalDetails(), "非法人员"),
        "7": (InputReportReasonPornography(), "非法组织"),
        "8": (InputReportReasonSpam(), "垃圾邮件"),
        "9": (InputReportReasonViolence(), "暴力行为")
    }

    while True:  # 外层循环
        try:
            # 获取举报目标信息
            if 'report_user' not in locals():  # 第一次运行或选择新用户时
                report_user = await get_user_input("请输入要举报的用户名或ID: ")
                # 获取举报类型
                print("\n举报原因选项:")
                for x in range(len(reportReasons)):
                    print(f"{x+1}:{reportReasons[x]}")
                report_type_input = await get_user_input("\n请选择举报原因(输入数字)：")
                
                if report_type_input not in report_type_map:
                    print("无效的选择，程序将退出...")
                    return
                
                report_type, reason_text = report_type_map[report_type_input]
                print(f"\n已选择举报原因: {reason_text}")
            
            # 每次都需要输入的信息
            report_count = int(await get_user_input("请输入要举报的次数: "))
            report_msg = await get_user_input("请输入举报内容：")
            
            success_count = 0
            batch_size = 5  # 每批处理的任务数
            
            # 获取所有可用的会话文件
            session_files = []
            for file in os.listdir(sen_dir):
                base_name, ext = os.path.splitext(file)
                is_dir = os.path.isdir(os.path.join(sen_dir + "/" + base_name))
                
                if ext == ".session" or is_dir:
                    s_dir = sen_dir + "/" + base_name + ".session"
                    if is_dir:
                        s_dir = sen_dir + "/" + base_name + "/" + base_name + ".session"
                    session_files.append((s_dir, base_name))
            
            if not session_files:
                print("没有找到可用的会话文件！")
                return
            
            # 处理所有会话文件，需要时重复使用
            while True:
                for i in range(0, len(session_files), batch_size):
                    if success_count == report_count and report_count != 0:
                        break
                    
                    # 获取当前批次的会话文件
                    batch = session_files[i:i + batch_size]
                    tasks = []
                    
                    for session_path, account_name in batch:
                        task = report_task(
                            session_path, account_name, report_user,
                            report_type, reason_text, report_msg, report_count
                        )
                        tasks.append(task)
                    
                    # 执行当前批次的任务
                    results = await asyncio.gather(*tasks, return_exceptions=True)
                    
                    # 统计成功次数
                    batch_success = sum(1 for r in results if r is True)
                    success_count += batch_success
                    
                    # 显示进度
                    if report_count == 0:
                        print(f"\n当前进度: 已成功 {success_count} 次")
                    else:
                        remaining = report_count - success_count
                        print(f"\n当前进度: {success_count}/{report_count} (还需{remaining}次)")
                    
                    # 批次间延迟
                    await asyncio.sleep(2)
                
                # 检查是否需要继续循环
                if report_count == 0 or success_count >= report_count:
                    break
                
                print("\n已用完所有账号，开始重新使用账号继续举报...")
                await asyncio.sleep(1)
            
            # 举报完成后的选择
            print(f"\n✨ 举报任务完成，总计成功举报 {success_count} 次")
            print("\n" + "="*50)
            print("💡 您可以选择:")
            print("1. ⭐ 继续举报当前用户")
            print(f"   当前用户: {report_user}")
            print(f"   举报类型: {reason_text}")
            print("\n2. 🔄 举报新的用户")
            print("\n3. ❌ 退出程序")
            print("="*50)
            
            while True:
                choice = await get_user_input("\n请输入您的选择(1-3): ")
                if choice in ['1', '2', '3']:
                    break
                print("❌ 无效的选择，请重新输入")
            
            if choice == '3':
                print("\n✨ 感谢使用，程序即将退出...")
                await asyncio.sleep(1)
                break
            elif choice == '2':
                print("\n🔄 切换到新用户举报...")
                await asyncio.sleep(1)
                del report_user  # 删除当前用户信息，触发重新输入
                continue
            else:  # choice == '1'
                print(f"\n⭐ 继续举报用户: {report_user}")
                print(f"当前举报类型: {reason_text}")
                continue  # 直接继续使用当前用户信息
                
        except Exception as e:
            print(f"\n❌ 程序执行出错: {str(e)}")
            choice = await get_user_input("\n是否要继续？(y/n): ")
            if choice.lower() != 'y':
                break

if __name__ == "__main__":
    asyncio.run(main())
