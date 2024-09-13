<!--
 * @Author: SudemQaQ
 * @Date: 2024-07-27 07:38:24
 * @email: mail@szhcloud.cn
 * @Blog: https://blog.szhcloud.cn
 * @github: https://github.com/sang8052
 * @LastEditors: SudemQaQ
 * @LastEditTime: 2024-09-12 13:07:48
 * @Description: 
-->
<template>
  <div>
    <t-card class="list-card-container" bordered>
      <t-row>
        <t-col :span="10">
          <t-form style="margin-top: 16px" labelWidth="200px" ref="DomainDetail">
            <template v-for="item in config_system">
              <t-form-item :label="item.desc" :key="item.item_name" style="width: 1000px">
                <t-input v-if="item.item_type == 'text'" v-model="item.item_value" />
                <t-button theme="default" variant="outline" v-if="item.item_type == 'html'" @click="on_text_edit(item)"
                  >点击编辑</t-button
                >
                <t-switch v-if="item.item_type == 'bool'" v-model="item.item_value" />
              </t-form-item>
            </template>
          </t-form>
        </t-col>
        <t-col :span="2">
          <t-button @click="btn_save_config">保存配置</t-button>
        </t-col>
      </t-row>
    </t-card>
      <tckeditor :content="edit_content"  :show="showEditor" @onClose="set_editor_content"></tckeditor>
  </div>
</template>
<script>
import { config_query,config_update_list } from '@/api';
import Tckeditor from './components/tckeditor.vue';
import log from '@/utils/log';

export default {
  components: {
    Tckeditor
  },
  data() {
    return {
      config_system: [],
      showEditor: false,
      edit:null,
      edit_content:'',
      config_item:"",
    };
  },
  mounted() {
    this.query_system_config();
  },
  methods: {
    async query_system_config() {
      const res = await config_query({ page_num: 1, page_size: 100 });
      this.config_system = [];
      res.data.data.forEach((item) => {
        if (item.item_type === 'bool') {
          item.item_value = item.item_value === '1';
        }
        this.config_system.push(item);
      });
      this.config_system = res.data.data;
    },
    async btn_save_config() {
      const configs = [];
      this.config_system.forEach((item)=>{
        if (item.item_type === 'bool') {
          if(item.item_value) item.item_value = '1';
          else item.item_value = '0';
        }
        configs.push(item);
      })
      const res = await config_update_list({configs});
      if(res.code === 0)this.$message.success("操作成功");
      this.query_system_config();
      
    },
    set_editor_content(content){
      this.edit_content   = content;
      this.config_system.forEach((item,index)=>{
        if(item.item_name === this.config_item){
          this.config_system[index].item_value = this.edit_content;
        }
      })
      this.showEditor = false;
      log.info(`保存配置项目[${this.config_item}]的配置`)
    },

    on_text_edit(item) {
      this.edit_content =item.item_value;
      this.showEditor = true;
      this.config_item = item.item_name;
    },
  },
};
</script>
