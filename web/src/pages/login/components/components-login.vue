<template>
  <t-form
    ref="form"
    :class="['item-container', `login-${type}`]"
    :data="formData"
    :rules="FORM_RULES"
    label-width="0"
    @submit="onSubmit"
  >
    <template v-if="type == 'password'">
      <t-form-item name="account">
        <t-input v-model="formData.username" size="large" placeholder="请输入账号">
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
          key="password"
          placeholder="请输入登录密码"
        >
          <template #prefix-icon>
            <lock-on-icon />
          </template>
          <template #suffix-icon>
            <browse-icon v-if="showPsw" @click="showPsw = !showPsw" key="browse" />
            <browse-off-icon v-else @click="showPsw = !showPsw" key="browse-off" />
          </template>
        </t-input>
      </t-form-item>

     
    </template>

    <t-form-item v-if="type !== 'qrcode'" class="btn-container">
      <t-button block :loading="btn_loading" size="large" type="submit"> 登录 </t-button>
    </t-form-item>

  
  </t-form>
</template>
<script lang="ts">
import Vue from 'vue';
import { UserIcon, LockOnIcon, BrowseOffIcon, BrowseIcon } from 'tdesign-icons-vue';
import {user_login} from '@/api';

const FORM_RULES = {
  username: [{ required: true, message: '账号必填', type: 'error' }],
  password: [{ required: true, message: '密码必填', type: 'error' }],
};
/** 高级详情 */
export default Vue.extend({
  name: 'Login',
  components: {
    UserIcon,
    LockOnIcon,
    BrowseOffIcon,
    BrowseIcon,
  },
  data() {
    return {
      FORM_RULES,
      type: 'password',
      formData: { username:"",password:"" },
      showPsw: false,
      countDown: 0,
      intervalTimer: null,
      btn_loading:false,
    };
  },
  beforeDestroy() {
    clearInterval(this.intervalTimer);
  },
  methods: {
    switchType(val) {
      this.type = val;
      this.$refs.form.reset();
    },
    async onSubmit({ validateResult }) {
      if (validateResult === true) {
        this.btn_loading = true;
        const res = await user_login({username:this.formData.username,password:this.formData.password});
        if(res.code === 0){
          this.$message.success("登录成功");
          window.localStorage.setItem("user_session",JSON.stringify(res.data));
          window.localStorage.setItem("user_session_id",res.data.session_id);
          await this.$store.dispatch("socketio/close_socket")
          await this.$store.dispatch("socketio/init_socket")
          this.$router.push({path:"/admin"});
        }
        this.btn_loading = false;
       
      }
    },
   
    handleCounter() {
      this.countDown = 60;
      this.intervalTimer = setInterval(() => {
        if (this.countDown > 0) {
          this.countDown -= 1;
        } else {
          clearInterval(this.intervalTimer);
          this.countDown = 0;
        }
      }, 1000);
    },
  },
});
</script>
