<template>
    <t-form
      ref="form"
      :class="['item-container', `register-${type}`]"
      :data="formData"
      :rules="FORM_RULES"
      label-width="0"
      @submit="onSubmit"
    >
    
 
        <t-form-item name="email">
            <t-input v-model="formData.username" type="text" size="large" placeholder="请输入您的用户名">
            <template #prefix-icon>
                <user-icon />
            </template>
            </t-input>
        </t-form-item>
    
  
      <t-form-item name="password">
        <t-input
          v-model="formData.password"
          size="large"
          :type="showPsw ? 'text' : 'password'"
          clearable
          placeholder="请输入登录密码"
        >
          <template #prefix-icon>
            <lock-on-icon />
          </template>
          <template #suffix-icon>
            <browse-icon v-if="showPsw" key="browse" @click="showPsw = !showPsw" />
            <browse-off-icon v-else key="browse-off" @click="showPsw = !showPsw" />
          </template>
        </t-input>
      </t-form-item>

      <t-form-item name="password_verify">
        <t-input
          v-model="formData.password_verify"
          size="large"
          :type="showPsw ? 'text' : 'password'"
          clearable
          placeholder="请再次输入一遍密码"
        >
          <template #prefix-icon>
            <lock-on-icon />
          </template>
          <template #suffix-icon>
            <browse-icon v-if="showPsw" key="browse" @click="showPsw_verify = !showPsw_verify" />
            <browse-off-icon v-else key="browse-off" @click="showPsw_verify = !showPsw_verify" />
          </template>
        </t-input>
      </t-form-item>
  

      <t-form-item name="nickname">
        <t-input v-model="formData.nickname" type="text" size="large" placeholder="请输入您的昵称">
        <template #prefix-icon>
            <surprised1-icon/>
        </template>
        </t-input>
    </t-form-item>

      <t-form-item name="mail_address">
        <t-input v-model="formData.mail_address" type="text" size="large" placeholder="请输入您的邮箱,用于接收证书签发状态通知">
        <template #prefix-icon>
            <mail-icon />
        </template>
        </t-input>
        </t-form-item>
      
  
      <t-form-item>
        <t-button block :loading="btn_loading" size="large" type="submit"> 注册 </t-button>
      </t-form-item>
  
    </t-form>
  </template>
<script lang="ts">
import Vue from 'vue';
import { UserIcon, MailIcon, BrowseIcon, BrowseOffIcon, LockOnIcon,Surprised1Icon } from 'tdesign-icons-vue';
import { user_reg } from '../../../api';
  
const INITIAL_DATA = {
  mail_address: '',
  password_verify:'',
  password: '',
  username: '',
  nickname:''
};
  
const FORM_RULES = {
  username: [{ required: true, message: '请输入您的用户名', type: 'error' }],
  nickname: [{ required: true, message: '请输入您的昵称', type: 'error' }],  
  mail_address: [{ required: true, email: true, message: '邮箱地址格式不正确', type: 'error' }],
  password: [{ required: true, message: '请输入您的密码,长度不小于8位',len:8,type: 'error' }],
};
  
/** 高级详情 */
export default Vue.extend({
  name: 'Register',
  components: {
    UserIcon,
    MailIcon,
    BrowseIcon,
    BrowseOffIcon,
    LockOnIcon,
    Surprised1Icon
  },
  data() {
    return {
      FORM_RULES,
      formData: { ...INITIAL_DATA },
      showPsw: false,
      showPsw_verify:false,
      btn_loading:false
    };
  },

  methods: {

    async onSubmit({ validateResult }: { validateResult: boolean }) {
      if (validateResult === true) {
      
        if(this.formData.password !== this.formData.password_verify) this.message.error("两次输入的密码不一致!")
        else{
          this.btn_loading = true;
          const res = await user_reg(this.formData);
          if(res.code === 0){
            this.$message.success('注册成功,请重新登陆!');
            this.$emit("reg_success");
          }
          else this.$message.error(res.msg);
          this.btn_loading = false;
        }
      }
    },
   
    
  },
});
</script>