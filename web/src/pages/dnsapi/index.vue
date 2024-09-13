<template>
<div>
    <t-card class="list-card-container" bordered style="height: 780px">
      <t-row justify="space-between">
        <t-col :span="8">
          <div style="width:100%">
            <t-select
              label="秘钥类型:"
              clearable
              v-model="search.key_type"
              :options="system_support"
              placeholder="请选择秘钥类型"
              style="width: 250px; float: left"
              :onChange="load_dnsapi_list"
            />
            <t-input   placeholder="请输入搜索关键字" :onChange="load_dnsapi_list"  v-model="search.keyword" style="width: 250px;float: left;margin-left: 16px;"  clearable  @clear="item_keyword = ''">
              <template #suffixIcon>
                <search-icon :style="{ cursor: 'pointer' }" />
               </template>
            </t-input>
          </div>
          
         
        </t-col>
        <t-col :span="4">
          <t-button
         
            style="float: right; margin-top: 4px"
            @click="on_create_key()"
            type="button"
          >
            <add-icon slot="icon" /> 添加API秘钥
          </t-button>
        </t-col>
      </t-row>

      <div class="table-container" style="height: 666px;margin-top: 16px;">
        <t-table rowKey="id" :columns="columns" :data="data" :loading="data_loading" >
          <template #action="{ row }">
            <t-link  theme="primary" @click="on_detail(row,'view')">详情</t-link>
            <t-link theme="warning" @click="on_detail(row,'edit')">修改</t-link>
            <t-link  theme="danger" @click="on_detail(row,'delete')">删除</t-link>
          </template>
        </t-table>
      </div>
      <t-pagination
        :showPageSize="false"
        :total="page_total"
        :defaultPageSize="page_size"
        :defaultCurrent="page_num"
        @change="on_pagination_change"
      />
    </t-card>

    <t-dialog
    :visible.sync="display_detail"
        :header="header_title"
        top="48px"
        width="720px"
    >
         <t-form style="margin-top: 16px" :data="api_detail" labelWidth="150px" ref="ApiDetail" :rules="form_rules" >
            <t-form-item label="秘钥名称" name="key_name">
                <t-input v-model="api_detail.key_name"  placeholder="请输入秘钥名称" :readonly="dialog_type == 'view'" />
            </t-form-item>

            <t-form-item label="秘钥类型" name="key_name">
                <t-select clearable  v-model="api_detail.key_type" :options="system_support"  placeholder="请选择秘钥类型" />
            </t-form-item>

            <t-form-item label="AccessId" name="access_id">
                <t-input v-model="api_detail.access_id"  placeholder="请输入秘钥的AccessId" :readonly="dialog_type == 'view'" />
            </t-form-item>

            <t-form-item label="AccessKey" name="access_key">
                <t-input v-model="api_detail.access_key"  placeholder="请输入秘钥的AccessKey" :readonly="dialog_type == 'view'" />
            </t-form-item>

         </t-form>
    <div slot="footer" style="margin-top: -16px;">
      <t-button type="button" theme="primary" :loading="btn_loading"   @click="on_submit()" v-if="dialog_type == 'create'">新增</t-button>
      <t-button type="button" theme="primary" :loading="btn_loading"  @click="on_submit()" v-if="dialog_type == 'edit'">保存</t-button>
      <t-button type="button" theme="default" :loading="btn_loading"  @click="on_close()"  v-if="dialog_type != 'view'">取消</t-button>

    </div>
    </t-dialog>
</div>
</template>
<script>
import log from '@/utils/log';
import { dnsapi_system_support,dnsapi_data_query,dnsapi_data_create,dnsapi_data_update,dnsapi_data_delete,dnsapi_data_detail } from '@/api';
import { AddIcon,SearchIcon} from 'tdesign-icons-vue';


export default{  
  components:{AddIcon,SearchIcon},
  data(){
    return {
      page_num:1,
      page_size:10,
      page_total:0,
      data:[],
      data_loading:false,
      btn_loading:false,
      columns:[
        { colKey: 'key_name', title: '秘钥名称', width: 150, fixed: 'left', ellipsis: true, align: 'center' },
        { colKey: 'key_type', title: '秘钥类型', width: 150, fixed: 'left', ellipsis: true, align: 'center' },
        { colKey: 'access_id', title: 'AccessId', width: 250, fixed: 'left', ellipsis: true, align: 'left' },
        { colKey: 'access_key', title: 'AccessKey', width: 250, fixed: 'left', ellipsis: true, align: 'left' },
        { colKey: 'action', title: '操作', align: 'left', fixed: 'right', width: 300 },

      ],
      search:{keyword:"",key_type:""},
      system_support:[],
      header_title:"",
      display_detail:false,
      api_detail:{id:"",key_name:"",key_type:"",access_id:"",access_key:""},
      dialog_type:"",
      form_rules:{
        key_name: [{ required: true, message: '秘钥名称必填', type: 'error' }],
        key_type: [{ required: true, message: '秘钥类型必选', type: 'error' }],
        access_id: [{ required: true, message: 'AccessId必填', type: 'error' }],
        access_key: [{ required: true, message: 'AccessKey必填', type: 'error' }],
      }
    }
  },
  created(){
    this.load_system_suport();
    this.load_dnsapi_list();
  },
  methods:{
    async load_dnsapi_list(){
      this.data_loading = true;
      const querys = {keyword:this.search.keyword,key_type:this.search.key_type,page_num:this.page_num,page_size:this.page_size};
      const res = await dnsapi_data_query(querys);
      log.success("拉取dnsapi 列表成功",res.data);
      this.data = res.data.data;
      this.data_loading = false;
      this.page_num = res.data.page_num;
      this.page_size =res.data.page_size;
      this.page_total = res.data.total ;

    },
    async load_system_suport(){
      const res= await dnsapi_system_support();
      this.system_support = [];
      res.data.forEach((item)=>{
        const option = {"label":item.name,"value":item.api_keyword};
        this.system_support.push(option);
      })
      log.success("拉取系统支持的dns_api 成功",this.system_support);
    },
    on_pagination_change(page){
      this.page_num = page.current;
      this.page_size = page.pageSize;
      this.load_dnsapi_list();
    },
    on_create_key(){
      this.display_detail = true;
      this.header_title = "新增API秘钥";
      this.$refs.ApiDetail.reset();
      this.dialog_type = "create";
        
    },
    on_close(){
      this.load_dnsapi_list();
      this.display_detail = false;
    },
    async on_detail(row,type){
      if(type === 'delete'){
        const dialog = this.$dialog.confirm({
          header: '提示',
          body: '此操作不可逆,确认执行?',
          confirmBtn: '确定',
          cancelBtn: '取消',
          onConfirm: async () => {
            const res = await dnsapi_data_delete(row.id);
            if (res.code === 0) {
              this.$message.success('删除API秘钥成功!');
              this.on_close();
            }
            dialog.hide();
          },
          onClose: async () => {
            dialog.hide();
          },
        });
      }
      else{
        const res = await dnsapi_data_detail(row.id);
        this.api_detail = res.data;
        this.display_detail = true;
        this.dialog_type = type;
        if(type === 'edit') this.header_title = '编辑API秘钥';
        else this.header_title = '查看API秘钥';
      }
    },
    async on_submit(){
      const validate = await this.$refs.ApiDetail.validate();
      if(typeof(validate) === typeof(true)){
        if(this.dialog_type === "create"){
          const payload =  {...this.api_detail};
          this.btn_loading =true;
          const  res = await dnsapi_data_create(payload);
          if(res.code === 0) this.$message.success(res.msg);
          this.btn_loading = false;
          this.on_close();
        }
        if(this.dialog_type === 'edit'){
          const payload = {...this.api_detail};
          this.btn_loading =true;
          const  res = await dnsapi_data_update(payload.id,payload);
          if(res.code === 0) this.$message.success(res.msg);
          this.btn_loading = false;
          this.on_close();
        }
      }
    }
   
  }
}
</script>