<template>
  <el-upload
    drag
    style="height: 130px; width: 96%; margin-left: 2%; margin-top: 10px"
    multiple
    action="#"
    ref="upload"
    :auto-upload="false"
    :on-change="createForm"
    :show-file-list="false"
  >
    <div @click="handelPre">
      <el-icon class="el-icon--upload" style="width: 1em; height: 1em"
        ><upload-filled
      /></el-icon>
      <div class="el-upload__text">
        Drop file here or <em>click to upload</em>
      </div>
    </div>
  </el-upload>
  <div style="margin-top: 75px; width: 100%">
    <el-select
      style="margin-left: 2%; width: 20%"
      placeholder="模型选择"
      @change="switchModel"
      v-model="modelList.id"
    >
      <el-option
        v-for="item in modelList"
        :key="item.id"
        :label="item.modelName"
        :value="item.value"
      ></el-option>
    </el-select>
    <el-select
      style="margin-left: 2%; width: 20%"
      placeholder="上传内容"
      v-model="uploadKinds.id"
      @change="switchUploadKind"
    >
      <el-option
        v-for="item in uploadKinds"
        :key="item.id"
        :value="item.value"
        :label="item.name"
      >
      </el-option>
    </el-select>
    <el-button
      style="margin-left: 44%; width: 10%; z-index: 9999"
      plain
      @click="predictFiles()"
    >
      确认测试</el-button
    >
  </div>
</template>

<script>
import { ElUpload, ElSelect, ElOption, ElButton } from "element-plus";
import { UploadFilled } from "@element-plus/icons-vue";
import axios from "axios";

export default {
  name: "localPicSelect",
  components: { ElUpload, UploadFilled, ElOption, ElSelect, ElButton },
  data() {
    return {
      // imgFile: {
      //   imageData: "",
      //   imgUrl: "",
      // },
      base64File: "",
      base64List: [],
      uploadKind: "",
      model: "",
      apiUrl: "",
      modelList: [
        {
          modelName: "Efficientnet",
          value: "custom_efficientnet",
          id: "1",
        },
        {
          modelName: "MoCoV3 aug+",
          value: "custom_efficientnet",
          id: "2",
        },
      ],
      uploadKinds: [
        {
          id: "1",
          value: "single predict",
          name: "单一图片",
        },
        {
          id: "2",
          value: "folder",
          name: "多文件上传",
        },
      ],
      uploadFile: {},
    };
  },
  methods: {
    createForm(item) {
      //使用FileReader方法读取上传文件并转化为base64格式
      console.log("文件信息", item);
      let reader = new FileReader();
      reader.readAsDataURL(item.raw);
      reader.onload = () => {
        console.log(reader.result);
        this.base64File = reader.result;
        this.base64List.push(reader.result);
      };
    },
    switchModel(value) {
      this.model = value;
    },
    switchUploadKind(value) {
      this.uploadKind = value;
    },
    predictFiles() {
      //console.log(this.uploadKind, this.model);
      if (this.uploadKind && this.model) {
        this.uploadFile.modelName = this.model;
        this.uploadFile.mode = this.uploadKind;
        if (this.uploadFile.mode == "single predict") {
          this.uploadFile.path = this.base64File;
          this.apiUrl = "http://localhost:8080/api/predict";
        } else {
          this.uploadFile.path = this.base64List;
          this.apiUrl = "http://localhost:8080/api/predictGroup";
        }

        console.log(this.uploadFile); //生成post请求携带的表单

        axios({
          method: "post",
          data: this.uploadFile,
          url: this.apiUrl,
        }).then((res) => {
          console.log(res.data);
          if (this.uploadFile.mode == "single predict") {
            this.$emit("predictResult", res.data, this.base64File);
          } else {
            this.$emit("predictResult", res.data, this.base64List);
          }
          //清空上传内容
          this.uploadFile = {};
          this.$refs.upload.clearFiles();
        });
      } else {
        alert("请先选择模型与上传方式");
      }
    },
  },
};
</script>
<style scoped>
svg {
  width: 88px;
  height: 88px;
}
</style>
