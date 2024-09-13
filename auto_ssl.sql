

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for sys_config
-- ----------------------------
DROP TABLE IF EXISTS `sys_config`;
CREATE TABLE `sys_config`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `item_value` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `item_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `create_time` bigint(20) NULL DEFAULT NULL,
  `update_time` bigint(20) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 17 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_config
-- ----------------------------
INSERT INTO `sys_config` VALUES (1, 'acme_root_path', '', 'acme的文件夹绝对路径', 'text', 1721388902, 1726117924);
INSERT INTO `sys_config` VALUES (2, 'acme_support_servers', '[\"letsencrypt\",\"zerossl\",\"buypass\",\"ssl.com\",\"google\"]', 'acme支持的服务器', 'text', 1721388902, 1726117924);
INSERT INTO `sys_config` VALUES (3, 'acme_key_length', '4096', 'acme签发证书时私钥长度', 'text', 1721388902, 1726117924);
INSERT INTO `sys_config` VALUES (4, 'mail_cert_title', 'SSL证书签发结果通知', '通知邮件的标题', 'text', 1721388902, 1726117924);
INSERT INTO `sys_config` VALUES (5, 'mail_cert_template_success', '<!DOCTYPE html>\n<html lang=\"zh-cn\" xmlns:v=\"urn:schemas-microsoft-com:vml\" xmlns:o=\"urn:schemas-microsoft-com:office:office\"><head><meta charset=\"utf-8\"><meta name=\"x-apple-disable-message-reformatting\"><meta http-equiv=\"x-ua-compatible\" content=\"ie=edge\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><meta name=\"format-detection\" content=\"telephone=no, date=no, address=no, email=no\"><!--[if mso]>\n    <style>\n        td,th,div,p,a,h1,h2,h3,h4,h5,h6 {font-family: \"Segoe UI\", sans-serif; mso-line-height-rule: exactly;}\n    </style>\n    <![endif]--><title>ACME_AutoSSL-邮件通知</title><style>.hover-underline:hover{text-decoration:underline!important}@keyframes spin{to{transform:rotate(360deg)}}@keyframes ping{100%,75%{transform:scale(2);opacity:0}}@keyframes pulse{50%{opacity:.5}}@keyframes bounce{0%,100%{transform:translateY(-25%);animation-timing-function:cubic-bezier(.8,0,1,1)}50%{transform:none;animation-timing-function:cubic-bezier(0,0,.2,1)}}@media (max-width:600px){.sm-inline-block{display:inline-block!important}.sm-leading-32{line-height:32px!important}.sm-px-0{padding-left:0!important;padding-right:0!important}.sm-px-24{padding-left:24px!important;padding-right:24px!important}.sm-py-32{padding-top:32px!important;padding-bottom:32px!important}.sm-pb-32{padding-bottom:32px!important}.sm-w-full{width:100%!important}}</style></head><body style=\"margin:0;padding:0;width:100%;word-break:break-word;-webkit-font-smoothing:antialiased;--bg-opacity:1;background-color:#eceff1;background-color:rgba(236,239,241,var(--bg-opacity))\"><div role=\"article\" aria-roledescription=\"email\" aria-label=\"Promotional Mail\" lang=\"en\"><figure class=\"table\" style=\"width:100%;\"><table style=\"font-family:Montserrat,-apple-system,\'Segoe UI\',sans-serif;\" width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" role=\"presentation\"><tbody><tr><td style=\"background-color:rgba(236,239,241,var(--bg-opacity));font-family:Montserrat,-apple-system,\'Segoe UI\',sans-serif;text-align:center;\"><figure class=\"table\" style=\"width:600px;\"><table class=\"sm-w-full\" style=\"font-family:Montserrat,Arial,sans-serif;\" width=\"600\" cellpadding=\"0\" cellspacing=\"0\" role=\"presentation\"><tbody><tr><td class=\"sm-px-24\" style=\"font-family:Montserrat,Arial,sans-serif;text-align:center;\"><figure class=\"table\" style=\"width:100%;\"><table style=\"font-family:Montserrat,Arial,sans-serif;\" width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" role=\"presentation\"><tbody><tr><td class=\"sm-px-24\" style=\"--bg-opacity:1;--text-opacity:1;background-color:rgba(255,255,255,var(--bg-opacity));border-radius:4px;color:rgba(98,98,98,var(--text-opacity));font-family:Montserrat,-apple-system,\'Segoe UI\',sans-serif;font-size:14px;line-height:24px;padding:48px;text-align:left;\" align=\"left\"><p style=\"--text-opacity:1;color:rgba(255,88,80,var(--text-opacity));font-size:20px;margin-top:0;\"><strong>&nbsp;</strong></p><p class=\"sm-leading-32\" style=\"--text-opacity:1;color:rgba(38,50,56,var(--text-opacity));font-size:20px;margin:0 0 24px;\"><strong>SSL 证书签发结果通知</strong></p><p style=\"font-size:1rem;margin:0 0 24px;\">我们很高兴的通知您,您于 &nbsp;{{cert_create_time}}&nbsp; 申请签发的SSL 证书已经签发成功了！</p><p style=\"font-size:1rem;margin:0 0 24px;\">以下是您的证书详情:</p><figure class=\"table\"><table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\"><tbody><tr><td style=\"text-align:right;\" width=\"25%\">证书域名:</td><td width=\"5%\">&nbsp;</td><td style=\"text-align:left;\" width=\"70%\">{{cert_reg_domain}}</td></tr><tr><td style=\"text-align:right;\" width=\"25%\">证书序列号:</td><td width=\"5%\">&nbsp;</td><td style=\"text-align:left;\" width=\"70%\">{{cert_serial_number}}</td></tr><tr><td style=\"text-align:right;\" width=\"25%\">证书签名算法:</td><td width=\"5%\">&nbsp;</td><td style=\"text-align:left;\" width=\"70%\">{{cert_signature_algorithm}}</td></tr><tr><td style=\"text-align:right;\" width=\"25%\">证书签发机构:</td><td width=\"5%\">&nbsp;</td><td style=\"text-align:left;\" width=\"70%\">{{cert_common_name}}</td></tr><tr><td style=\"text-align:right;\" width=\"25%\">证书签发时间:</td><td width=\"5%\">&nbsp;</td><td style=\"text-align:left;\" width=\"70%\">{{cert_reg_time}}</td></tr><tr><td style=\"text-align:right;\" width=\"25%\">证书过期时间:</td><td width=\"5%\">&nbsp;</td><td style=\"text-align:left;\" width=\"70%\">{{cert_expire_time}}</td></tr></tbody></table></figure><p style=\"font-size:1rem;margin:0 0 24px;\">证书的私钥和证书文件已经随附邮件发送,您可以直接下载!</p><p style=\"margin:0 0 16px;\">收件人:{{mail_send_to}}<br><i>发信时间: {{current_time}}</i></p></td></tr><tr><td style=\"--text-opacity:1;color:rgba(236,239,241,var(--text-opacity));font-family:Montserrat,-apple-system,\'Segoe UI\',sans-serif;font-size:12px;text-align:center;\"><p style=\"--text-opacity:1;color:rgba(38,50,56,var(--text-opacity));\">ACME_AutoSSL <a target=\"_blank\" rel=\"noopener noreferrer\" href=\"https://github.com/sang8052/acme_autossl\">https://github.com/sang8052/acme_autossl</a> version:{{current_app_version}}</p></td></tr><tr><td style=\"font-family:Montserrat,Arial,sans-serif;height:16px;\" height=\"16\">&nbsp;</td></tr></tbody></table></figure></td></tr></tbody></table></figure></td></tr></tbody></table></figure></div></body></html>', '签发成功的邮件模板', 'html', 1721388902, 1726117924);
INSERT INTO `sys_config` VALUES (6, 'mail_cert_template_error', '<!DOCTYPE html>\n<html lang=\"zh-cn\" xmlns:v=\"urn:schemas-microsoft-com:vml\" xmlns:o=\"urn:schemas-microsoft-com:office:office\"><head><meta charset=\"utf-8\"><meta name=\"x-apple-disable-message-reformatting\"><meta http-equiv=\"x-ua-compatible\" content=\"ie=edge\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><meta name=\"format-detection\" content=\"telephone=no, date=no, address=no, email=no\"><!--[if mso]>\n    <style>\n        td,th,div,p,a,h1,h2,h3,h4,h5,h6 {font-family: \"Segoe UI\", sans-serif; mso-line-height-rule: exactly;}\n    </style>\n    <![endif]--><title>ACME_AutoSSL-邮件通知</title><style>.hover-underline:hover{text-decoration:underline!important}@keyframes spin{to{transform:rotate(360deg)}}@keyframes ping{100%,75%{transform:scale(2);opacity:0}}@keyframes pulse{50%{opacity:.5}}@keyframes bounce{0%,100%{transform:translateY(-25%);animation-timing-function:cubic-bezier(.8,0,1,1)}50%{transform:none;animation-timing-function:cubic-bezier(0,0,.2,1)}}@media (max-width:600px){.sm-inline-block{display:inline-block!important}.sm-leading-32{line-height:32px!important}.sm-px-0{padding-left:0!important;padding-right:0!important}.sm-px-24{padding-left:24px!important;padding-right:24px!important}.sm-py-32{padding-top:32px!important;padding-bottom:32px!important}.sm-pb-32{padding-bottom:32px!important}.sm-w-full{width:100%!important}}</style></head><body style=\"margin:0;padding:0;width:100%;word-break:break-word;-webkit-font-smoothing:antialiased;--bg-opacity:1;background-color:#eceff1;background-color:rgba(236,239,241,var(--bg-opacity))\"><div role=\"article\" aria-roledescription=\"email\" aria-label=\"Promotional Mail\" lang=\"en\"><figure class=\"table\" style=\"width:100%;\"><table style=\"font-family:Montserrat,-apple-system,\'Segoe UI\',sans-serif;\" width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" role=\"presentation\"><tbody><tr><td style=\"background-color:rgba(236,239,241,var(--bg-opacity));font-family:Montserrat,-apple-system,\'Segoe UI\',sans-serif;text-align:center;\"><figure class=\"table\" style=\"width:600px;\"><table class=\"sm-w-full\" style=\"font-family:Montserrat,Arial,sans-serif;\" width=\"600\" cellpadding=\"0\" cellspacing=\"0\" role=\"presentation\"><tbody><tr><td class=\"sm-px-24\" style=\"font-family:Montserrat,Arial,sans-serif;text-align:center;\"><figure class=\"table\" style=\"width:100%;\"><table style=\"font-family:Montserrat,Arial,sans-serif;\" width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" role=\"presentation\"><tbody><tr><td class=\"sm-px-24\" style=\"--bg-opacity:1;--text-opacity:1;background-color:rgba(255,255,255,var(--bg-opacity));border-radius:4px;color:rgba(98,98,98,var(--text-opacity));font-family:Montserrat,-apple-system,\'Segoe UI\',sans-serif;font-size:14px;line-height:24px;padding:48px;text-align:left;\" align=\"left\"><p style=\"--text-opacity:1;color:rgba(255,88,80,var(--text-opacity));font-size:20px;margin-top:0;\"><strong>&nbsp;</strong></p><p class=\"sm-leading-32\" style=\"--text-opacity:1;color:rgba(38,50,56,var(--text-opacity));font-size:20px;margin:0 0 24px;\"><strong>SSL 证书签发结果通知</strong></p><p style=\"font-size:1rem;margin:0 0 24px;\">我们很抱歉的通知您,您于 &nbsp;{{cert_create_time}}&nbsp; 申请签发的SSL 证书签发失败!<br>您申请签发的域名为:{{cert_reg_domain}}<br>您可以下载附件中的签发日志查看进一步的内容<br>&nbsp;</p><p style=\"margin:0 0 16px;\">收件人:{{mail_send_to}}<br><i>发信时间: {{current_time}}</i></p></td></tr><tr><td style=\"--text-opacity:1;color:rgba(236,239,241,var(--text-opacity));font-family:Montserrat,-apple-system,\'Segoe UI\',sans-serif;font-size:12px;text-align:center;\"><p style=\"--text-opacity:1;color:rgba(38,50,56,var(--text-opacity));\">ACME_AutoSSL <a target=\"_blank\" rel=\"noopener noreferrer\" href=\"https://github.com/sang8052/acme_autossl\">https://github.com/sang8052/acme_autossl</a> version:{{current_app_version}}</p></td></tr><tr><td style=\"font-family:Montserrat,Arial,sans-serif;height:16px;\" height=\"16\">&nbsp;</td></tr></tbody></table></figure></td></tr></tbody></table></figure></td></tr></tbody></table></figure></div></body></html>', '签发失败的邮件模板', 'html', 1721388902, 1726117924);
INSERT INTO `sys_config` VALUES (7, 'smtp_server_host', '', 'smtp 的服务器地址', 'text', 1721388856, 1726117924);
INSERT INTO `sys_config` VALUES (8, 'smtp_server_port', '', 'smtp 的服务器端口号', 'text', 1721388845, 1726117924);
INSERT INTO `sys_config` VALUES (9, 'smtp_server_ssl', '0', 'smtp 是否启用ssl', 'bool', 1721388902, 1726117924);
INSERT INTO `sys_config` VALUES (10, 'smtp_user_username', '', 'smtp 的用户名', 'text', 1721388834, 1726117924);
INSERT INTO `sys_config` VALUES (11, 'smtp_user_password', '', 'smtp 的密码', 'text', 1721388874, 1726117924);
INSERT INTO `sys_config` VALUES (12, 'smtp_user_nickname', '', 'smtp 的发送人昵称', 'text', 1721388902, 1726117924);
INSERT INTO `sys_config` VALUES (13, 'callback_sign_token', '', '回调请求的签名密钥', 'text', 1721388902, 1726117924);

-- ----------------------------
-- Table structure for sys_dns_api
-- ----------------------------
DROP TABLE IF EXISTS `sys_dns_api`;
CREATE TABLE `sys_dns_api`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `api_keyword` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `api_id_field` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `api_key_field` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `create_time` int(11) NULL DEFAULT NULL,
  `update_time` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_dns_api
-- ----------------------------
INSERT INTO `sys_dns_api` VALUES (1, '阿里云', 'dns_ali', 'Ali_Key', 'Ali_Secret', 1721388638, NULL);
INSERT INTO `sys_dns_api` VALUES (2, '腾讯云', 'dns_tencent', 'Tencent_SecretId', 'Tencent_SecretKey', 1721388638, NULL);
INSERT INTO `sys_dns_api` VALUES (3, 'Cloudfare', 'dns_cf', 'CF_Email', 'CF_Key', 1721388638, NULL);

-- ----------------------------
-- Table structure for sys_task
-- ----------------------------
DROP TABLE IF EXISTS `sys_task`;
CREATE TABLE `sys_task`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NULL DEFAULT NULL,
  `cert_id` int(11) NULL DEFAULT NULL,
  `status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `pid` int(11) NULL DEFAULT NULL,
  `tmp_uuid` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `reg_path` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `create_time` bigint(20) NULL DEFAULT NULL,
  `update_time` bigint(20) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 93 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_task
-- ----------------------------


-- ----------------------------
-- Table structure for sys_user
-- ----------------------------
DROP TABLE IF EXISTS `sys_user`;
CREATE TABLE `sys_user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `mail_address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `nickname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `create_time` bigint(20) NULL DEFAULT NULL,
  `update_time` bigint(20) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_user
-- ----------------------------


-- ----------------------------
-- Table structure for user_cert
-- ----------------------------
DROP TABLE IF EXISTS `user_cert`;
CREATE TABLE `user_cert`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NULL DEFAULT NULL,
  `domain_id` int(11) NULL DEFAULT NULL,
  `prefix` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `callback_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `ssl_private_key` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `ssl_public_key` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `ssl_fullchain` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `serial_number` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `signature_algorithm` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `common_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `reg_time` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `expire_time` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `create_time` bigint(20) NULL DEFAULT NULL,
  `update_time` bigint(20) NULL DEFAULT NULL,
  `task_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 94 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_cert
-- ----------------------------

-- ----------------------------
-- Table structure for user_dns_api
-- ----------------------------
DROP TABLE IF EXISTS `user_dns_api`;
CREATE TABLE `user_dns_api`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NULL DEFAULT NULL,
  `key_type` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `key_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `access_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `access_key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `create_time` bigint(20) NULL DEFAULT NULL,
  `update_time` bigint(20) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_dns_api
-- ----------------------------


-- ----------------------------
-- Table structure for user_dns_domain
-- ----------------------------
DROP TABLE IF EXISTS `user_dns_domain`;
CREATE TABLE `user_dns_domain`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key_id` int(11) NULL DEFAULT NULL,
  `uid` int(11) NULL DEFAULT NULL,
  `domain` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `create_time` bigint(20) NULL DEFAULT NULL,
  `update_time` bigint(20) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 15 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_dns_domain
-- ----------------------------


SET FOREIGN_KEY_CHECKS = 1;
