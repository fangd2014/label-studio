export default {
  enableHotkeys: {
    newUI: {
      title: "标注快捷键",
      description: "启用快捷键快速选择标签",
    },
    description: "启用标注快捷键",
    onChangeEvent: "toggleHotkeys",
    defaultValue: true,
  },
  enableTooltips: {
    newUI: {
      title: "在提示中显示快捷键",
      description: "在工具与操作提示中显示按键绑定",
    },
    description: "显示快捷键提示",
    onChangeEvent: "toggleTooltips",
    checked: "",
    defaultValue: false,
  },
  enableLabelTooltips: {
    newUI: {
      title: "在标签上显示快捷键",
      description: "在标签上显示按键绑定",
    },
    description: "显示标签快捷键提示",
    onChangeEvent: "toggleLabelTooltips",
    defaultValue: true,
  },
  showLabels: {
    newUI: {
      title: "显示区域标签",
      description: "显示区域的标签名称",
    },
    description: "在区域内显示标签",
    onChangeEvent: "toggleShowLabels",
    defaultValue: false,
  },
  continuousLabeling: {
    newUI: {
      title: "创建区域后保持标签选中",
      description: "使用当前选中标签连续创建区域",
    },
    description: "创建区域后保持标签选中",
    onChangeEvent: "toggleContinuousLabeling",
    defaultValue: false,
  },
  selectAfterCreate: {
    newUI: {
      title: "创建后自动选中区域",
      description: "自动选中新创建的区域",
    },
    description: "创建后选中区域",
    onChangeEvent: "toggleSelectAfterCreate",
    defaultValue: false,
  },
  showLineNumbers: {
    newUI: {
      tags: "文本标签",
      title: "显示行号",
      description: "在文档中定位并引用具体文本行",
    },
    description: "为文本显示行号",
    onChangeEvent: "toggleShowLineNumbers",
    defaultValue: false,
  },
  preserveSelectedTool: {
    newUI: {
      tags: "图像标签",
      title: "保持已选工具",
      description: "在任务切换时保留当前工具",
    },
    description: "记住已选工具",
    onChangeEvent: "togglepreserveSelectedTool",
    defaultValue: true,
  },
  enableSmoothing: {
    newUI: {
      tags: "图像标签",
      title: "缩放时平滑像素",
      description: "放大时对图像像素进行平滑处理",
    },
    description: "缩放时启用图像平滑",
    onChangeEvent: "toggleSmoothing",
    defaultValue: true,
  },
  invertedZoom: {
    newUI: {
      tags: "图像标签",
      title: "反转缩放方向",
      description: "反转滚轮缩放方向",
    },
    description: "启用反向缩放",
    onChangeEvent: "toggleInvertedZoom",
    defaultValue: false,
  },
};
