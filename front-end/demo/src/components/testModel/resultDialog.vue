<template>
  <el-dialog
    v-model="resultVisible"
    width="800px"
    height="600px"
    @open="onOpen"
    @close="onClose"
  >
    <div style="display: flex">
      <!-- <el-button
        style="
          flex: 1;
          vertical-align: center;
          text-align: center;
          justify-content: center;
          height: 30px;
        "
      >
        left arrow 
        <el-icon class="el-icon--arrowleft" >
          <arrow-left />
        </el-icon>
      </el-button> -->
      <div
        style="flex: 4; text-align: center; vertical-align: top; height: 300px"
      >
        <span
          style="
            display: block;
            color: #2b2b2b;
            font-size: 24px;
            margin-bottom: 20px;
          "
          >测试图片</span
        >
        <el-image :src="currentPic" :fit="fill" style="width: 65%"></el-image>
      </div>
      <div
        style="
          flex: 4;
          margin-left: 20px;
          text-align: center;
          vertical-align: top;
          width: 45%;
        "
      >
        <span
          style="
            display: block;
            color: #2b2b2b;
            font-size: 24px;
            margin-bottom: 20px;
          "
          >测试结果</span
        >
        <span
          style="
            display: block;
            color: #2b2b2b;
            font-size: 36px;
            margin-bottom: 20px;
            margin-top: 120px;
          "
          >{{ this.currentResult }}</span
        >
      </div>
      <!-- <div style="flex: 1">
        right arrow 
        <el-button
          style="
            flex: 1;
            vertical-align: center;
            text-align: center;
            justify-content: center;
            height: 30px;
          "
        >
          <el-icon class="el-icon--arrowleft">
            <arrow-right />
          </el-icon>
        </el-button>
      </div> -->
    </div>
  </el-dialog>
</template>

<script>
import { List } from "echarts";
import { ElDialog, ElImage } from "element-plus";
// import { ArrowLeft, ArrowRight } from "@element-plus/icons-vue";

export default {
  name: "resultDialog",
  components: { ElDialog, ElImage },
  props: {
    result: { type: List },
    pic: { type: List },
  },
  data() {
    return {
      baseImg: "",
      currentPic: "",
    };
  },
  methods: {
    onOpen() {
      console.log(this.pic);
      if (this.pic instanceof Array) {
        this.currentPic = this.pic[0];
        this.currentResult = this.result[0];
      } else {
        this.currentPic = this.pic;
        this.currentResult = this.result;
      }
    },
    onClose() {},
  },
};
</script>
