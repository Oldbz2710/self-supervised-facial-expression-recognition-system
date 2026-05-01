<template>
  <div>
    <el-header
      class="title"
      style="
        height: 50px;
        background-color: #378dd6;
        top: -15px;
        width: 100%;
        color: #e6e6e6;
      "
    >
      <span class="titleLeft">
        <el-button
          text
          @click="onBack"
          style="
            border: none;
            margin-right: 5px;
            margin-bottom: 2px;
            color: #e6e6e6;
          "
          class="backButton"
        >
          <el-icon><Back /></el-icon>
          返回主页
        </el-button>
        <span style="padding-left: 5px; border-left: #e6e6e6 solid 1px">
          调用测试
        </span>
      </span>
    </el-header>
    <div
      style="
        margin-top: 7%;
        margin-left: 30%;
        width: 40%;
        height: 420px;
        background-color: #378dd6;
      "
    >
      <el-button
        primary
        @click="onTake"
        style="height: 150px; margin-top: 10px; width: 96%; margin-left: 2%"
      >
        拍照测试
      </el-button>
      <localPicSelect ref="localPicSelect" @predictResult="getResult" />
    </div>
    <!-- 页面组件部分 -->
    <el-dialog
      title="拍照上传"
      v-model="visible"
      @close="onCancel"
      width="1065px"
    >
      <div class="box">
        <video
          id="videoCamera"
          class="canvas"
          :width="videoWidth"
          :height="videoHeight"
          autoPlay
        ></video>
        <canvas
          id="canvasCamera"
          class="canvas"
          :width="videoWidth"
          :height="videoHeight"
        ></canvas>
      </div>
      <div>
        <el-button @click="drawImage" icon="el-icon-camera" size="small">
          拍照
        </el-button>
        <el-button
          v-if="open == 0"
          @click="getCompetence"
          icon="el-icon-video-camera"
          size="small"
        >
          打开摄像头
        </el-button>
        <el-button
          v-if="open == 1"
          @click="stopNavigator"
          icon="el-icon-switch-button"
          size="small"
        >
          关闭摄像头
        </el-button>
        <el-button @click="resetCanvas" icon="el-icon-refresh" size="small">
          重置
        </el-button>
        <el-button @click="onCancel" icon="el-icon-circle-close" size="small">
          取消
        </el-button>
        <el-button
          @click="onUpload"
          :loading="loading"
          type="primary"
          icon="el-icon-upload2"
          size="small"
        >
          上传
        </el-button>
      </div>
    </el-dialog>
    <resultDialog
      v-model="resultVisible"
      :result="predictResult"
      :pic="predictPic"
    />
  </div>
</template>
<script>
import { ElButton, ElHeader, ElDialog } from "element-plus";
import { Back } from "@element-plus/icons-vue";
import localPicSelect from "./localPicSelect.vue";
import resultDialog from "./resultDialog.vue";
import axios from "axios";

export default {
  name: "contrastMain",
  components: {
    ElHeader,
    ElButton,
    ElDialog,
    Back,
    localPicSelect,
    resultDialog,
  },
  data() {
    return {
      visible: false,
      open: 0,
      resultVisible: false,
      imgSrc: "",
      loading: false,
      camera: false,
      thisVideo: null,
      thisContext: null,
      thisCancas: null,
      videoWidth: 500,
      videoHeight: 400,
      //result界面
      predictResult: "",
      predictPic: "",
      uploadFile: {},
    };
  },
  methods: {
    onBack() {
      this.$router.go(-1);
    },
    //摄像调用
    onTake() {
      this.visible = true;
      this.getCompetence();
    },
    onCancel() {
      this.visible = false;
      this.resetCanvas();
      this.stopNavigator();
    },
    onUpload() {
      if (this.imgSrc) {
        // const file = this.imgSrc; // base64 to file
        // const time = new Date().valueOf(); //time
        // const name = time + ".png";
        // const conversions = this.dataURLtoFile(file, name);
        // const data = new FormData();
        // const Address = "";
        // data.append("file", conversions);
        // console.log(conversions);
        this.uploadFile.modelName = "custom_efficientnet";
        this.uploadFile.mode = "single predict";
        this.uploadFile.path = this.imgSrc;
        console.log(this.uploadFile);
        // const options = {
        //   method: "POST",
        //   body: data,
        //   headers: {
        //     Accept: "application/json",
        //   },
        // };
        // this.loading = true;
        // fetch(Address.UPLOAD, options)
        //   .then((response) => {
        //     return response.json();
        //   })
        //   .then((responseText) => {
        //     this.loading = false;
        //     if (responseText.code === 0) {
        //       this.imgSrc = responseText.data.src;
        //       this.$emit("getImg", responseText.data.src);
        //       this.onCancel();
        //       this.$notify({
        //         title: "上传成功",
        //         message: responseText.msg,
        //         type: "success",
        //       });
        //     }
        //   })
        //   .catch((error) => {
        //     this.loading = false;
        //     this.$notify.error({
        //       title: "上传失败",
        //       message: error.msg,
        //     });
        //   });
        axios({
          method: "post",
          url: "http://localhost:8080/api/predict",
          data: this.uploadFile,
          //补充form
        }).then((res) => {
          console.log(res.data);
          this.uploadFile = {};
          this.getResult(res.data, this.imgSrc);
          this.onCancel();
        });
      }
    },
    //权限获取，摄像头调用
    getCompetence() {
      this.$nextTick(() => {
        const _this = this;
        this.open = 1;
        this.thisCancas = document.getElementById("canvasCamera");
        this.thisContext = this.thisCancas.getContext("2d");
        this.thisVideo = document.getElementById("videoCamera");

        if (navigator.mediaDevices === undefined) {
          navigator.mediaDevices = {};
        }

        if (navigator.mediaDevices.getUserMedia === undefined) {
          navigator.mediaDevices.getUserMedia = function (constraints) {
            let getUserMedia =
              navigator.webkitGetUserMedia ||
              navigator.mozGetUserMedia ||
              navigator.getUserMedia;
            if (!getUserMedia) {
              return Promise.reject(
                new Error("getUserMedia is not implement in this broswer")
              );
            }
            return new Promise(function (resolve, reject) {
              getUserMedia.call(navigator, constraints, resolve, reject);
            });
          };
        }
        const constraints = {
          audio: false,
          video: {
            width: _this.videoWidth,
            height: _this.videoHeight,
            transform: "scaleX(-1)",
          },
        };
        navigator.mediaDevices
          .getUserMedia(constraints)
          .then(function (stream) {
            if ("srcObject" in _this.thisVideo) {
              _this.thisVideo.srcObject = stream;
            } else {
              _this.thisVideo.src = window.URL.createObjectURL(stream);
            }
            _this.thisVideo.onloadedmetadata = function () {
              _this.thisVideo.play();
            };
          });
      });
    },
    //canvas
    drawImage() {
      this.thisContext.drawImage(
        this.thisVideo,
        0,
        0,
        this.videoWidth,
        this.videoHeight
      );
      this.imgSrc = this.thisCancas.toDataURL("image/png");
      // let reader = new FileReader()
      //console.log(this.imgSrc);
    },
    // dataURLtoFile(dataurl, filename) {
    //   // console.log("dataurl", dataurl);
    //   let arr = dataurl.split(",");
    //   let mime = arr[0].match(/:(.*?);/)[1];
    //   console.log("mime", mime);
    //   let bstr = atob(arr[1]);
    //   console.log("bstr", bstr);
    //   let n = bstr.length;
    //   let u8arr = new Uint8Array(n);
    //   while (n--) {
    //     u8arr[n] = bstr.charCodeAt(n);
    //   }
    //   console.log("u8arr", u8arr);
    //   return new File([u8arr], filename, { type: mime });
    // },
    clearCanvas(id) {
      let c = document.getElementById(id);
      let cxt = c.getContext("2d");
      cxt.clearRect(0, 0, c.width, c.height);
    },
    resetCanvas() {
      this.imgSrc = "";
      this.clearCanvas("canvasCamera");
    },
    //close the camera
    stopNavigator() {
      if (this.thisVideo && this.thisVideo !== null) {
        this.thisVideo.srcObject.getTracks()[0].stop();
        this.open = 0;
        // console.log(this.open);
      }
    },

    //本地文件上传
    //从上传组件获取form

    //控制结果组件
    getResult(msg1, msg2) {
      this.predictResult = msg1;
      this.predictPic = msg2;
      console.log("url", this.predictPic);
      this.resultVisible = true;
    },
  },
};
</script>
<style scoped>
.title {
  width: 100%;
  display: flex;
}
.titleLeft {
  float: left;
  line-height: 50px;
  font-size: 18px;
}
.backButton :hover {
  color: #378dd6;
}
</style>
