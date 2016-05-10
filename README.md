# iOS-Package-Script
- 脚本功能介绍
    - 将iOS源代码打包发布到fir，然后向指定邮件地址发送邮件，并附带二维码。收到邮件的用户可以通过扫面二维码安装app
    - 支持两个target，每一个target可以有不用的配置、bundleID、开发证书，但是共用同一套代码。方便在同一台手机上安装线上和测试包进行对比
    - 建立分支
- 相关工具
    - 安装fir：https://github.com/FIRHQ/fir-cli/blob/master/README.md
- 工程文件需要的配置
    - 在Compile Sources之前添加一个Run Script，内容如下，其作用是将svn版本号写进Info.plist的CFBundleVersion字段
        - version=`svn info ${PROJECT_DIR} | grep Revision: | cut -c 11-`
        - /usr/libexec/PlistBuddy -c "Set :CFBundleVersion $version" ${PROJECT_DIR}/${TARGET_NAME}/Info.plist
- 打包命令的使用
    - NAME
        - package
    - SYNOPSIS
        - package [-tbrnml] [-p local path] [-u svn url] [-v svn version]
    - DESCRIPTION
        - -t     测试版
        - -b     只建立分支，不进行其他操作
        - -p     指定从本地的某个路径开始打包
        - -n  先update代码再进行其他操作
        - -u     默认从本地的固定路径开始打包，如果指定此参数，后面需要加svnURL，则从svnURL co代码编译
        - -r     默认是Debug模式，加此参数就是Release模式
        - -m     默认是发邮件，加此参数不发邮件
        - -l     默认是发布到fir，如果加上此参数，只进行本地打包，不发布
        - -v     默认是当前svn版本，此参数指定svn版本
- 各个文件的作用
    - package：shell脚本，负责打包、发布、调用发送邮件的python脚本
    - mail/updateEmail.py：发布成功时，向指定邮件地址发送通知邮件
    - mail/mailList.txt：接收发布成功通知的邮件地址列表，每行一个
    - mail/log.txt：本次发包要写的log
    - mail/alertEmail.py：操作失败时，向指定邮件地址发送通知邮件
    - mail/alertMailList.txt：接收操作失败通知的邮件地址列表，每行一个
