<!--
 * @Author: SudemQaQ
 * @Date: 2024-06-17 11:22:51
 * @email: mail@szhcloud.cn
 * @Blog: https://blog.szhcloud.cn
 * @github: https://github.com/sang8052
 * @LastEditors: SudemQaQ
 * @LastEditTime: 2024-06-19 22:20:50
 * @Description: 
-->
<template>
  <div class="result-fail">
    <error-circle-icon class="result-fail-icon" />
    <div class="result-fail-title">创建失败</div>
    <div class="result-fail-describe">抱歉，您的项目创建失败，请联系管理员...</div>
    <div>
      <t-button @click="() => $router.push('/')">返回首页</t-button>
    </div>
  </div>
</template>

<script>
import { ErrorCircleIcon } from 'tdesign-icons-vue';

export default {
  name: 'ResultFail',
  components: {
    ErrorCircleIcon,
  },
};
</script>

<style lang="less" scoped>
@import '@/style/variables.less';
.result-fail {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 75vh;

  &-icon {
    font-size: 72px;
    color: var(--td-text-color-secondary);
  }

  &-title {
    margin-top: 28px;
    font-size: 20px;
    color: var(--td-text-color-primary);
    text-align: center;
    line-height: 28px;
    font-weight: 500;
  }

  &-describe {
    margin: 8px 0 32px;
    font-size: 14px;
    color: var(--td-text-color-secondary);
    line-height: 22px;
  }
  .t-button + .t-button {
    margin-left: var(--td-comp-margin-s);
  }
}
</style>
