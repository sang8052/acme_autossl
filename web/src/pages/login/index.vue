<!--
 * @Author: SudemQaQ
 * @Date: 2024-06-17 11:22:51
 * @email: mail@szhcloud.cn
 * @Blog: https://blog.szhcloud.cn
 * @github: https://github.com/sang8052
 * @LastEditors: SudemQaQ
 * @LastEditTime: 2024-07-27 11:18:49
 * @Description: 
-->
<template>
  <div class="login-wrapper">

    <div class="login-container">
      <div class="title-container">
        <h1 class="title margin-no">登录到</h1>
        <h1 class="title">Acme_AutoSSL 签发中心</h1>
        <div class="sub-title">
          <p class="tip">{{ type == 'register' ? '已有账号?' : '没有账号吗?' }}</p>
          <p class="tip" @click="switchType(type == 'register' ? 'login' : 'register')">
            {{ type == 'register' ? '登录' : '注册新账号' }}
          </p>
        </div>
      </div>

      <login  v-if="type === 'login'" />
      <register v-else @reg_success="switchType('login')"  />
    </div>

    <footer class="copyright">Copyright @ 2020-{{new Date().getFullYear()}} atonal.cn. All Rights Reserved</footer>
  </div>
</template>
<script>
import Login      from './components/components-login.vue';
import Register   from './components/components-reg.vue';

export default {
  name: 'LoginIndex',
  components: {
    Login,Register
  },
  data() {
    return {
      type: "login"
    };
  },
  mounted(){
    const _type = this.$route.query.type;
    if(_type) this.type = _type;
    else this.type ='login';
    window.sessionStorage.removeItem("handle_user_unlogin");
  },
  methods: {
    switchType(val) {
      this.$router.push({path:"/login",query:{type:val}});
      this.type = val;
    },
  },
 
};
</script>
<style lang="less">
@import url('./index.less');
</style>
