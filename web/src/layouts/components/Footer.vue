<!--
 * @Author: SudemQaQ
 * @Date: 2024-06-17 11:22:51
 * @email: mail@szhcloud.cn
 * @Blog: https://blog.szhcloud.cn
 * @github: https://github.com/sang8052
 * @LastEditors: SudemQaQ
 * @LastEditTime: 2024-06-17 18:34:37
 * @Description: 
-->
<template>
  <div :class="prefix + '-footer'">Copyright © 2021-{{new Date().getFullYear()}} atonal.cn. All Rights Reserved</div>
</template>

<script>
import { prefix } from '@/config/global';
import Vue from 'vue';

export default Vue.extend({
  name: `${prefix}-footer`,
  data() {
    return {
      prefix,
    };
  },
});
</script>

<style lang="less" scoped>
@import '@/style/variables';

.@{starter-prefix}-footer {
  color: var(--td-text-color-placeholder);
  line-height: 20px;
  text-align: center;
}
</style>
