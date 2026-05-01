<template>
  <el-dialog
    v-model="detailVisible"
    @open="onOpen"
    style="width: 60%; height: 60%"
    ><div style="width: 94%; height: 94%; margin: 0 auto">
      <el-image
        :src="require(`../../assets/pic/structure/${currentSrc}`)"
        :fit="fill"
        style="margin-top: 5px"
      >
      </el-image>
    </div>
  </el-dialog>
</template>
<script>
import { ElDialog, ElImage } from "element-plus";

export default {
  name: "detailWindow",
  components: { ElDialog, ElImage },
  props: {
    modelUuid: { type: Int16Array },
  },
  data() {
    return {
      currentSrc: "SimCLR.png",
      structureSrc: [
        "SimCLR.png",
        "mocov1.png",
        "mocov2.png",
        "BYOL.png",
        "Simsiam.png",
        "mocov3.png",
        "Dino.png",
      ],
    };
  },
  methods: {
    onOpen() {
      this.currentSrc = this.structureSrc[this.modelUuid];
      console.log(this.currentSrc, this.modelUuid);
    },
  },
};
</script>
