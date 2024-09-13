
<template>
    <div>
      <t-card class="list-card-container" bordered>
      
        <t-form style="margin-top: 16px;margin-bottom: 32px;" labelWidth="200px" ref="userFrom"         >

            <t-form-item label="登录IP" key="currnet_device_ip" style="width: 1200px">
                <t-input  type="text" v-model="session.client_ip" @click="on_redirect_ipdb(session.client_ip)" readonly />
            </t-form-item>

            <t-form-item label="本次登录设备" key="currnet_login_device" style="width: 1200px">
                <t-input  type="text" v-model="session.user_agent" readonly />
            </t-form-item>

            <t-form-item label="登录时间" key="currnet_login_time" style="width: 1200px">
                <t-input  type="text" v-model="session.login_time" readonly />
            </t-form-item>

            <t-form-item label="昵称" key="user_nickname" style="width: 600px">
                <t-input  type="text" v-model="session.nickname"  />
                <t-button style="margin-left: 16px;" theme="default" variant="outline" @click="on_edit_user()" >保存</t-button>
            </t-form-item>

            <t-form-item label="邮箱地址" key="user_mail_address" style="width: 600px">
                <t-input  type="text" v-model="session.mail_address"  />
                <t-button style="margin-left: 16px;" theme="default" variant="outline" >保存</t-button>
            </t-form-item>

            <t-form-item label="原密码" key="user_password_old" style="width: 412px">
                <t-input  type="password" v-model="password.old"   />
            </t-form-item>

            <t-form-item label="新密码" key="user_password_new" style="width: 500px">
                <t-input  type="password" v-model="password.new"   />
                <t-button style="margin-left: 16px;" theme="default" variant="outline"   @click="on_update_password()">修改密码</t-button>
            </t-form-item>

        </t-form>

      </t-card>
    </div>
  </template>
<script>
import {user_session,user_update,user_resetpassword} from '@/api';
import log from '@/utils/log';
import dayjs from 'dayjs';

export default {

  data() {
    return {

      session:{client_ip:"",nickname:"",user_agent:"",mail_address:"",login_time:""},
      password:{
        old:"",
        new:""
      }
    };
  },
  mounted() {
    this.query_user_session();
  },
  methods: {
    async query_user_session(){
      const res = await user_session();
      this.session = res.data;
      const login_time = dayjs(this.session.login_time).format("YYYY-MM-DD HH:mm:ss");
      this.session.login_time = login_time;
    },
    on_redirect_ipdb(client_ip){
      log.info("查询ip 地址信息...");
      window.open(`https://tools.iw3c.com.cn/ip/?ip=${  client_ip}`);
    },
    async on_update_password(){
      if(this.password.new.length < 8) this.$message.error("新密码的长度不能小于8位");
      else if(this.password.old.length < 8) this.$message.error("旧密码的长度不能小于8位");
      else{
        const payload = {old_password:this.password.old,new_password:this.password.new};
        const res = await user_resetpassword(payload);

        if(res.code === 0){
          this.$message.success("重置密码成功,请重新登录");
          window.localStorage.removeItem("user_session");
          window.localStorage.removeItem("user_session_id");
          this.$router.push({path:"/login"});
        } 
      }
    }, 
    async on_edit_user(){
      const payload = {
        "mail_address":this.session.mail_address,
        "nickname":this.session.nickname
      }
      const res = await user_update(payload);
      if(res.code === 0) {
        this.$message.success("操作成功");
        const res = await user_session();
        window.localStorage.setItem("user_session",JSON.stringify(res.data));
        this.query_user_session();
      }
    }
  },
};
</script>
  