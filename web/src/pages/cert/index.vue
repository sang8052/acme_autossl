<template>
    <div>
        <t-card class="list-card-container" bordered style="height: 780px">
          <t-row justify="space-between">
            <t-col :span="8">
              <div style="width:100%">
                <t-select clearable  :onChange="load_cert_list" v-model="search.domain_id" :options="dns_domains" placeholder="请选择域名" style="width: 250px; float: left"/>
                <t-input   placeholder="请输入搜索关键字" :onChange="load_cert_list"  v-model="search.keyword" style="width: 250px;float: left;margin-left: 16px;"  clearable >
                  <template #suffixIcon>
                    <search-icon :style="{ cursor: 'pointer' }" />
                   </template>
                </t-input>
              </div>
              
             
            </t-col>
            <t-col :span="4">
              <t-button
             
                style="float: right; margin-top: 4px"
                @click="on_create_cert()"
                type="button"
              >
                <add-icon slot="icon" /> 签发新证书
              </t-button>
            </t-col>
          </t-row>
    
          <div class="table-container" style="height: 666px;margin-top: 16px;">
            <t-table rowKey="id" :columns="columns" :data="data" :loading="data_loading" >
              <template #action="{ row }">
                <t-link  theme="primary" @click="on_detail(row,'view')">详情</t-link>
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
            :onClose="on_close"
            :visible.sync="display_detail"
            :header="header_title"
            top="48px"
            width="1200px"
        >
            <t-loading :loading="detail_loading" />
         <t-form style="margin-top: 16px" :data="cert_detail" labelWidth="150px" ref="CertDetail" :rules="form_rules" >

            <t-form-item label="根域名" name="domain_id">
                <t-select clearable  v-model="cert_detail.domain_id" :options="dns_domains" placeholder="请选择根域名" :disabled="dialog_type == 'view'"/>
            </t-form-item>

            <t-form-item label="子域名" name="prefix">
                <t-input v-if="dialog_type=='create'" v-model="cert_detail.prefix"  placeholder="子域名必填,泛域名请填写_" :readonly="dialog_type == 'view'" />
                <span v-else  >{{cert_detail.prefix}}</span>
            </t-form-item>

            <t-form-item label="签发机构" name="acme_server" v-if="dialog_type=='create'">
              <t-select   clearable  :onChange="load_cert_list" v-model="cert_detail.acme_server" :options="acme_support_servers" placeholder="请选择域名" style="width: 250px; float: left"/>

            </t-form-item>


            <t-form-item label="状态" v-if="dialog_type == 'view'" >
               <span v-if="task_detail.status == 'running'" style="color: orange;" >签发中...</span>
               <span v-else-if="task_detail.status == 'error'" style="color: red;" >签发失败...</span>
               <span v-else style="color: green;" >签发成功</span>
            </t-form-item>


            <t-form-item v-if="!cert_detail.serial_number && dialog_type == 'view'" label="实时日志" >
              <div class="xtrem_container" style="margin:10px auto;width: 100%;height: 300px;overflow-y: hidden;">
                <div id="xtrem_console"  style="height: 300px;margin-left: 8px;margin-right: 8px;"  class="xterm"></div>
              </div>
            </t-form-item>


            <t-form-item v-if="cert_detail.serial_number" label="证书序列号" >
               <span >{{ cert_detail.serial_number }}</span>
            </t-form-item>

            <t-form-item v-if="cert_detail.serial_number" label="签名算法" >
               <span >{{ cert_detail.signature_algorithm }}</span>
            </t-form-item>

            <t-form-item v-if="cert_detail.serial_number" label="签发机构" >
               <span >{{ cert_detail.common_name }}</span>
            </t-form-item>

            <t-form-item v-if="cert_detail.serial_number" label="签发时间" >
               <span >{{ cert_detail.reg_time }}</span>
            </t-form-item>

            <t-form-item v-if="cert_detail.serial_number" label="到期时间" >
               <span >{{ cert_detail.expire_time }}</span>
            </t-form-item>

            <t-form-item v-if="cert_detail.ssl_private_key && cert_detail.ssl_fullchain" label="证书下载" >
               <span ><a @click="download_file_content(cert_detail.ssl_private_key,'private.key')">下载私钥</a>
                  <a @click="download_file_content(cert_detail.ssl_fullchain,'fullchain.pem')">下载证书</a>
                </span>
            </t-form-item>
           
        </t-form>
        <div slot="footer" style="margin-top: -16px;">
            <t-button type="button" theme="primary" :loading="btn_loading"   @click="on_submit()" v-if="dialog_type == 'create'">新增</t-button>
            <t-button type="button" theme="default" :loading="btn_loading"  @click="on_close()"   v-if="dialog_type == 'create'" >取消</t-button>
        </div>
        </t-dialog>
    </div>
</template>
<script>
import log from '@/utils/log';

import 'xterm/css/xterm.css'
import { Terminal } from 'xterm';
import { FitAddon } from "xterm-addon-fit";

import { AddIcon,SearchIcon} from 'tdesign-icons-vue';

import {cert_data_query,domain_data_query,cert_data_create,cert_data_delete,cert_data_detail,task_status} from "@/api"
import { config_detail } from '../../api';

export default{
  components:{AddIcon,SearchIcon},
  data(){
    return {
      page_num:1,
      page_size:10,
      page_total:0,
      search:{domain_id:"",keyword:""},
      dns_domains:[],
      cert_detail:{prefix:"",domain_id:"",id:"",serial_number:""},
      task_detail:{},
      display_detail:false,
      header_title:"",
      btn_loading:false,
      dialog_type:"",
      data:[],
      acme_support_servers:[],
      columns:[
        { colKey: 'prefix', title: '子域名', width: 100, fixed: 'left', ellipsis: true, align: 'left' },
        { colKey: 'domain', title: '根域名', width: 150, fixed: 'left', ellipsis: true, align: 'left' },
        { colKey: 'expire_time', title: '过期时间', width: 180, fixed: 'left', ellipsis: true, align: 'left' },
        { colKey: 'serial_number', title: '证书序列号', width: 330, fixed: 'left', ellipsis: true, align: 'left' },
        { colKey: 'signature_algorithm', title: '签名算法', width: 200, fixed: 'left', ellipsis: true, align: 'left' },
        { colKey: 'common_name', title: '签发机构', width: 270, fixed: 'left', ellipsis: true, align: 'left' },
        { colKey: 'action', title: '操作', align: 'left', fixed: 'right', width: 200 },
      ],
      data_loading:false,
      task_log:"",
      form_rules:{
        prefix: [{ required: true, message: '子域名必填,泛域名请填写_', type: 'error' }],
        domain_id: [{ required: true, message: '请选择签发证书的根域名', type: 'error' }],
        acme_server:[{ required: true, message: '请选择SSL签发机构', type: 'error' }],
      },
      refresh:false,
      detail_loading:false,
      socket_handle:null,
    }
  },
  created(){
    this.load_cert_server();
    this.load_domain_list();
    this.load_cert_list();
  },

  methods:{
    async load_cert_server(){
      const res = await config_detail("acme_support_servers");
      this.acme_support_servers = []
      const support_servers =  JSON.parse(res.data.item_value);
      support_servers.forEach((item)=>{
        const option = {"label":item,"value":item};
        this.acme_support_servers.push(option);
      });
    },
    async load_domain_list(){
      const res = await domain_data_query({page_num:1,page_size:9999});
      this.dns_domains = [];
      res.data.data.forEach((item)=>{
        const option = {"label":item.domain,"value":item.id};
        this.dns_domains.push(option);
      })
    },
    async load_cert_list(){
      this.data_loading = false;
      const res = await cert_data_query({page_num:this.page_num,page_size:this.page_size,domain_id:this.search.domain_id,keyword:this.search.keyword});
      this.data = res.data.data;
      this.data_loading = false;
      this.page_num = res.data.page_num;
      this.page_size =res.data.page_size;
      this.page_total = res.data.total ;
    },
    on_pagination_change(page){
      this.page_num = page.current;
      this.page_size = page.pageSize;
      this.load_cert_list();
    },
    on_create_cert(){
      this.display_detail = true;
      this.header_title = '签发新证书';
      this.dialog_type = 'create';
      this.$refs.CertDetail.reset();
      this.cert_detail = {};
      this.cert_detail.acme_server = this.acme_support_servers[0].value;

    },
    async on_detail(row,type){
      if(type === 'delete'){
        const dialog = this.$dialog.confirm({
          header: '提示',
          body: '此操作不可逆,确认执行?',
          confirmBtn: '确定',
          cancelBtn: '取消',
          onConfirm: async () => {
            const res = await cert_data_delete(row.id);
            if (res.code === 0) {
              this.$message.success('删除证书信息成功!');
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
        this.cert_detail = row;
        this.display_detail = true;
        this.dialog_type = type;
        this.header_title = '查看证书详情';
        this.detail_loading = true;
        await this.get_cert_detail();
        this.detail_loading = false;
      }
    },
    on_close(){
      this.load_cert_list();
      this.display_detail = false;
      if(this.refresh) clearInterval(this.refresh);
    },
    async on_submit(){
      const validate = await this.$refs.CertDetail.validate();
      if(typeof(validate) === typeof(true)){
        const payload =  {...this.cert_detail};
        this.btn_loading =true;
        const  res = await cert_data_create(payload);
        if(res.code === 0) {
          this.$message.success(res.msg);
          this.cert_detail.id = res.data.cert_id;
          this.dialog_type = 'view';
          this.tag_log = "";
          this.get_cert_detail();
        }
        this.btn_loading = false;
        
      }
    },
    async get_cert_detail(){
      // 拿到证书的任务id
      let res = await cert_data_detail(this.cert_detail.id);
      const {task_id} = res.data;
      this.cert_detail = res.data;
      log.info(`当前证书的task_id:${  task_id}`);

      res =await task_status(task_id);
      this.task_detail = res.data;
      if(this.task_detail.status === 'running'){

        // 通过socket 获得任务状态
        const socket_client = this.$store.getters["socketio/client"];
        const fitAddon = new FitAddon();
        this.term = new Terminal({
          rendererType: "canvas",
          rows: 20,
          cols:60,
          convertEol: true, 
          fontSize: 14, 
          disableStdin: true,
          scrollback: 30,
          tabStopWidth: 4,
          cursorBlink:true,
          cursorStyle: 'underline', 
        });
        this.term.loadAddon(fitAddon);
        this.term.open(document.getElementById("xtrem_console"));
        fitAddon.fit(); 
        
        socket_client.off("terminal");
        log.info("开始监听terminal事件!")
        socket_client.on("terminal",async (msg)=>{
          const payload = JSON.parse(msg);
          if(payload.task_id === task_id){
            // line_id 为 -1 表示任务执行结束了
            if(payload.line_id === -1){
              const {content} = payload;
              this.task_detail = content.task;
              this.cert_detail = content.cert;
              socket_client.off("terminal");
              this.dialog_type = "view";
              this.header_title = "查看证书详情";
            }
            // 处理日志逻辑
            else{
              this.term.writeln(payload.content);
              this.term.focus(); 
              this.term.scrollToBottom();
            }
          }
          else log.warning(`收到其它任务详情,task_id:${  payload.task_id}`);
        })
        
      }

     
    },
    download_file_content(content,filename){
      const blob = new Blob([content], {type: 'text/plain'})
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }
  }
}
</script>
<style>
.xterm-screen{
  min-height: calc(100vh);
}
.xtrem_container :state(--webkit-scrollbar) {
  width:8px;height:8px
}

.xtrem_container :state(--webkit-scrollbar-thumb) {
  border:2px solid transparent;
  background-clip:content-box;
  background-color:var(--td-scrollbar-color);
  border-radius:15px
}


</style>