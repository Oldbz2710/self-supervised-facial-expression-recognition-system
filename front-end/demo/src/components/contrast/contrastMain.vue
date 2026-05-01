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
          模型对比
        </span>
      </span>
    </el-header>
    <el-table :data="tableData" style="width: 100%" border="True">
      <el-table-column fixed type="index" width="50" />
      <el-table-column prop="name" label="模型名称" style="width: 15%" />
      <el-table-column prop="advantage" label="模型优势" style="width: 20%" />
      <el-table-column prop="methods" label="学习方式" style="width: 15%" />
      <el-table-column prop="backBone" label="骨干网络" style="width: 15%" />
      <el-table-column
        prop="lossFunction"
        label="损失函数"
        style="width: 15%"
      />
      <el-table-column
        fixed="right"
        label="操作"
        min-width="120"
        align="center"
      >
        <template #default="scope">
          <el-button
            type="primary"
            size="small"
            @click="checkModelDetail(scope)"
          >
            查看模型结构
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
  <detailWindow v-model="detailVisible" :model-uuid="modelUuid" />
</template>
<script>
import { ElHeader, ElButton, ElTable, ElTableColumn } from "element-plus";
import detailWindow from "./detailWindow.vue";

export default {
  name: "contrastMain",
  components: { ElHeader, ElButton, ElTable, ElTableColumn, detailWindow },
  data() {
    return {
      detailVisible: false,
      modelUuid: "",
      tableData: [
        {
          id: 0,
          name: "SimCLR",
          advantage: "首次在无监督学习中引入mlp层作为Projector",
          methods: "简单对比学习",
          backBone: "Resnet 50",
          lossFunction: "NCE",
        },
        {
          id: 1,
          name: "MoCo",
          advantage:
            "采用动量编码器优化原有的memory bank，构造了足够大且具有一致性的字典队列",
          methods: "基于动量对比的自监督学习",
          backBone: "Resnet 50",
          lossFunction: "Info NCE",
        },
        {
          id: 2,
          name: "MoCo V2",
          advantage:
            "借鉴SimCLR模型，在动量编码器提取特征后添加mlp层进行非线性变化",
          methods: "基于动量对比的自监督学习",
          backBone: "Resnet 50",
          lossFunction: "Info NCE",
        },
        {
          id: 3,
          name: "BYOL",
          advantage: "首次提出无负样本的对比学习方法，正负样本训练队列非对称",
          methods: "无负样本对比学习",
          backBone: "Resnet 50",
          lossFunction: "alignment + uniformity",
        },
        {
          id: 4,
          name: "SimSiam",
          advantage:
            "结构更加简单，证明了stop-gradient对避免无负样本对比学习模型坍塌的重要性",
          methods: "无负样本对比学习",
          backBone: "Resnet 50",
          lossFunction: "MSE loss",
        },
        {
          id: 5,
          name: "MoCo V3",
          advantage:
            "在MoCoV2的基础上更换骨干网络为ViT，同时证明了冻结ViT的patch projection层对训练稳定性的提升",
          methods: "基于动量对比自监督学习",
          backBone: "Vision Transformer",
          lossFunction: "Info NCE",
        },
        {
          id: 6,
          name: "DINO",
          advantage:
            "在BYOL的基础上进行改进，并研究了自监督学习对ViT feature的影响",
          methods: "无标签自蒸馏方法",
          backBone: "Vision Transformer，Swin Transformer",
          lossFunction: "cross entropy",
        },
      ],
    };
  },
  methods: {
    onBack() {
      this.$router.go(-1);
    },
    checkModelDetail(scope) {
      this.detailVisible = true;
      // console.log(scope.row.name);
      this.modelUuid = scope.row.id;
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
