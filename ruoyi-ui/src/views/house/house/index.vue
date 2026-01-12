<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" size="small" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="房源编号" prop="houseId">
        <el-input
          v-model="queryParams.houseId"
          placeholder="请输入房源编号"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="房源编码" prop="houseCode">
        <el-input
          v-model="queryParams.houseCode"
          placeholder="请输入房源编码"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="房源标题" prop="title">
        <el-input
          v-model="queryParams.title"
          placeholder="请输入房源标题"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="小区名称" prop="community">
        <el-input
          v-model="queryParams.community"
          placeholder="请输入小区名称"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="城市" prop="city">
        <el-select v-model="queryParams.city" placeholder="请选择城市" clearable>
          <el-option
            v-for="dict in dict.type.house_city"
            :key="dict.value"
            :label="dict.label"
            :value="dict.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="镇" prop="town">
        <el-select v-model="queryParams.town" placeholder="请选择镇" clearable>
          <el-option
            v-for="dict in dict.type.house_town"
            :key="dict.value"
            :label="dict.label"
            :value="dict.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="户型" prop="houseType">
        <el-select v-model="queryParams.houseType" placeholder="请选择户型" clearable>
          <el-option
            v-for="dict in dict.type.house_type"
            :key="dict.value"
            :label="dict.label"
            :value="dict.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="朝向" prop="orientation">
        <el-select v-model="queryParams.orientation" placeholder="请选择朝向" clearable>
          <el-option
            v-for="dict in dict.type.house_orientation"
            :key="dict.value"
            :label="dict.label"
            :value="dict.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="楼层高度" prop="floorHeight">
        <el-input
          v-model="queryParams.floorHeight"
          placeholder="请输入楼层高度"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="楼层类型" prop="floorType">
        <el-select v-model="queryParams.floorType" placeholder="请选择楼层类型" clearable>
          <el-option
            v-for="dict in dict.type.house_floor_type"
            :key="dict.value"
            :label="dict.label"
            :value="dict.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="建筑年代" prop="buildingYear">
        <el-input
          v-model="queryParams.buildingYear"
          placeholder="请输入建筑年代"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="装修类型" prop="decorationType">
        <el-select v-model="queryParams.decorationType" placeholder="请选择装修类型" clearable>
          <el-option
            v-for="dict in dict.type.house_decoration_type"
            :key="dict.value"
            :label="dict.label"
            :value="dict.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="房源标签" prop="tags">
        <el-input
          v-model="queryParams.tags"
          placeholder="请输入房源标签"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="产权性质" prop="propertyRightType">
        <el-select v-model="queryParams.propertyRightType" placeholder="请选择产权性质" clearable>
          <el-option
            v-for="dict in dict.type.house_property_right_type"
            :key="dict.value"
            :label="dict.label"
            :value="dict.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="产权年限" prop="propertyRightYear">
        <el-select v-model="queryParams.propertyRightYear" placeholder="请选择产权年限" clearable>
          <el-option
            v-for="dict in dict.type.house_property_right_year"
            :key="dict.value"
            :label="dict.label"
            :value="dict.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="物业类型" prop="propertyType">
        <el-select v-model="queryParams.propertyType" placeholder="请选择物业类型" clearable>
          <el-option
            v-for="dict in dict.type.house_property_type"
            :key="dict.value"
            :label="dict.label"
            :value="dict.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery">搜索</el-button>
        <el-button icon="el-icon-refresh" size="mini" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button
          type="primary"
          plain
          icon="el-icon-plus"
          size="mini"
          @click="handleAdd"
          v-hasPermi="['house:house:add']"
        >新增
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="el-icon-edit"
          size="mini"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['house:house:edit']"
        >修改
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="el-icon-delete"
          size="mini"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['house:house:remove']"
        >删除
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="el-icon-download"
          size="mini"
          @click="handleExport"
          v-hasPermi="['house:house:export']"
        >导出
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="info"
          plain
          icon="el-icon-upload2"
          size="mini"
          @click="handleImport"
          v-hasPermi="['house:house:import']"
        >导入
        </el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList" :columns="columns"></right-toolbar>
    </el-row>

    <el-table :loading="loading" :data="houseList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center"/>
      <el-table-column label="房源编号" :show-overflow-tooltip="true" v-if="columns[0].visible" prop="houseId"/>
      <el-table-column label="房源编码" align="center" :show-overflow-tooltip="true" v-if="columns[1].visible"
                       prop="houseCode"/>
      <el-table-column label="封面图片" align="center" v-if="columns[2].visible" prop="coverImage" width="100">
        <template slot-scope="scope">
          <image-preview :src="scope.row.coverImage" :width="50" :height="50"/>
        </template>
      </el-table-column>
      <el-table-column label="房源标题" align="center" :show-overflow-tooltip="true" v-if="columns[3].visible"
                       prop="title"/>
      <el-table-column label="小区名称" align="center" :show-overflow-tooltip="true" v-if="columns[4].visible"
                       prop="community"/>
      <el-table-column label="小区地址" align="center" :show-overflow-tooltip="true" v-if="columns[5].visible"
                       prop="address"/>
      <el-table-column label="所属区域" align="center" :show-overflow-tooltip="true" v-if="columns[6].visible"
                       prop="area"/>
      <el-table-column label="城市" align="center" v-if="columns[7].visible" prop="city">
        <template slot-scope="scope">
          <dict-tag :options="dict.type.house_city" :value="scope.row.city"/>
        </template>
      </el-table-column>
      <el-table-column label="镇" align="center" v-if="columns[8].visible" prop="town">
        <template slot-scope="scope">
          <dict-tag :options="dict.type.house_town" :value="scope.row.town"/>
        </template>
      </el-table-column>
      <el-table-column label="总价" align="center" :show-overflow-tooltip="true" v-if="columns[9].visible"
                       prop="totalPrice"/>
      <el-table-column label="单价" align="center" :show-overflow-tooltip="true" v-if="columns[10].visible"
                       prop="unitPrice"/>
      <el-table-column label="户型" align="center" v-if="columns[11].visible" prop="houseType">
        <template slot-scope="scope">
          <dict-tag :options="dict.type.house_type" :value="scope.row.houseType"/>
        </template>
      </el-table-column>
      <el-table-column label="建筑面积" align="center" :show-overflow-tooltip="true" v-if="columns[12].visible"
                       prop="areaSize"/>
      <el-table-column label="朝向" align="center" v-if="columns[13].visible" prop="orientation">
        <template slot-scope="scope">
          <dict-tag :options="dict.type.house_orientation" :value="scope.row.orientation"/>
        </template>
      </el-table-column>
      <el-table-column label="楼层" align="center" :show-overflow-tooltip="true" v-if="columns[14].visible"
                       prop="floor"/>
      <el-table-column label="楼层高度" align="center" :show-overflow-tooltip="true" v-if="columns[15].visible"
                       prop="floorHeight"/>
      <el-table-column label="装修面积单价" align="center" :show-overflow-tooltip="true" v-if="columns[16].visible"
                       prop="decorationArea"/>
      <el-table-column label="楼层类型" align="center" v-if="columns[17].visible" prop="floorType">
        <template slot-scope="scope">
          <dict-tag :options="dict.type.house_floor_type" :value="scope.row.floorType"/>
        </template>
      </el-table-column>
      <el-table-column label="建筑年代" align="center" :show-overflow-tooltip="true" v-if="columns[18].visible"
                       prop="buildingYear"/>
      <el-table-column label="装修类型" align="center" v-if="columns[19].visible" prop="decorationType">
        <template slot-scope="scope">
          <dict-tag :options="dict.type.house_decoration_type" :value="scope.row.decorationType"/>
        </template>
      </el-table-column>
      <el-table-column label="房源标签" align="center" :show-overflow-tooltip="true" v-if="columns[20].visible"
                       prop="tags">
        <template slot-scope="scope">
          <div v-if="scope.row.tags && scope.row.tags.trim() !== ''" style="display: flex; flex-wrap: wrap; gap: 4px;">
            <el-tag
              v-for="(tag, index) in scope.row.tags.split(';').filter(item => item.trim() !== '')"
              :key="index"
              size="small">
              {{ tag.trim() }}
            </el-tag>
          </div>
          <span v-else>无</span>
        </template>
      </el-table-column>
      <el-table-column label="产权性质" align="center" v-if="columns[21].visible" prop="propertyRightType">
        <template slot-scope="scope">
          <dict-tag :options="dict.type.house_property_right_type" :value="scope.row.propertyRightType"/>
        </template>
      </el-table-column>
      <el-table-column label="产权年限" align="center" v-if="columns[22].visible" prop="propertyRightYear">
        <template slot-scope="scope">
          <dict-tag :options="dict.type.house_property_right_year" :value="scope.row.propertyRightYear"/>
        </template>
      </el-table-column>
      <el-table-column label="房源介绍" align="center" :show-overflow-tooltip="true" v-if="columns[23].visible"
                       prop="houseIntro"/>
      <el-table-column label="房源图片" align="center" v-if="columns[24].visible" prop="imageUrls" width="100">
        <template slot-scope="scope">
          <image-preview separator=";" :src="scope.row.imageUrls" :width="50" :height="50"/>
        </template>
      </el-table-column>
      <el-table-column label="物业类型" align="center" v-if="columns[25].visible" prop="propertyType">
        <template slot-scope="scope">
          <dict-tag :options="dict.type.house_property_type" :value="scope.row.propertyType"/>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="text"
            icon="el-icon-edit"
            @click="handleUpdate(scope.row)"
            v-hasPermi="['house:house:edit']"
          >修改
          </el-button>
          <el-button
            size="mini"
            type="text"
            icon="el-icon-delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['house:house:remove']"
          >删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination
      v-show="total>0"
      :total="total"
      :page.sync="queryParams.pageNum"
      :limit.sync="queryParams.pageSize"
      @pagination="getList"
    />

    <!-- 添加或修改房源信息对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="500px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="房源编号" prop="houseId">
          <el-input :readonly="isUpdate" v-model="form.houseId" placeholder="请输入房源编号"/>
        </el-form-item>
        <el-form-item label="房源编码" prop="houseCode">
          <el-input v-model="form.houseCode" placeholder="请输入房源编码"/>
        </el-form-item>
        <el-form-item label="封面图片" prop="coverImage">
          <image-upload separator=";" :limit="1" v-model="form.coverImage"/>
        </el-form-item>
        <el-form-item label="房源标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入房源标题"/>
        </el-form-item>
        <el-form-item label="小区名称" prop="community">
          <el-input v-model="form.community" placeholder="请输入小区名称"/>
        </el-form-item>
        <el-form-item label="小区地址" prop="address">
          <el-input v-model="form.address" placeholder="请输入小区地址"/>
        </el-form-item>
        <el-form-item label="所属区域" prop="area">
          <el-input v-model="form.area" placeholder="请输入所属区域"/>
        </el-form-item>
        <el-form-item label="城市" prop="city">
          <el-select v-model="form.city" placeholder="请选择城市">
            <el-option
              v-for="dict in dict.type.house_city"
              :key="dict.value"
              :label="dict.label"
              :value="dict.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="镇" prop="town">
          <el-select v-model="form.town" placeholder="请选择镇">
            <el-option
              v-for="dict in dict.type.house_town"
              :key="dict.value"
              :label="dict.label"
              :value="dict.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="总价" prop="totalPrice">
          <el-input-number :precision="2" v-model="form.totalPrice" placeholder="请输入总价"/>
        </el-form-item>
        <el-form-item label="单价" prop="unitPrice">
          <el-input-number :precision="2" v-model="form.unitPrice" placeholder="请输入单价"/>
        </el-form-item>
        <el-form-item label="户型" prop="houseType">
          <el-select v-model="form.houseType" placeholder="请选择户型">
            <el-option
              v-for="dict in dict.type.house_type"
              :key="dict.value"
              :label="dict.label"
              :value="dict.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="建筑面积" prop="areaSize">
          <el-input-number :precision="2" v-model="form.areaSize" placeholder="请输入建筑面积"/>
        </el-form-item>
        <el-form-item label="朝向" prop="orientation">
          <el-select v-model="form.orientation" placeholder="请选择朝向">
            <el-option
              v-for="dict in dict.type.house_orientation"
              :key="dict.value"
              :label="dict.label"
              :value="dict.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="楼层" prop="floor">
          <el-input v-model="form.floor" placeholder="请输入楼层"/>
        </el-form-item>
        <el-form-item label="楼层高度" prop="floorHeight">
          <el-input-number v-model="form.floorHeight" placeholder="请输入楼层高度"/>
        </el-form-item>
        <el-form-item label="面积单价" prop="decorationArea">
          <el-input-number :precision="2" v-model="form.decorationArea" placeholder="请输入装修面积单价"/>
        </el-form-item>
        <el-form-item label="楼层类型" prop="floorType">
          <el-select v-model="form.floorType" placeholder="请选择楼层类型">
            <el-option
              v-for="dict in dict.type.house_floor_type"
              :key="dict.value"
              :label="dict.label"
              :value="dict.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="建筑年代" prop="buildingYear">
          <el-input-number v-model="form.buildingYear" placeholder="请输入建筑年代"/>
        </el-form-item>
        <el-form-item label="装修类型" prop="decorationType">
          <el-select v-model="form.decorationType" placeholder="请选择装修类型">
            <el-option
              v-for="dict in dict.type.house_decoration_type"
              :key="dict.value"
              :label="dict.label"
              :value="dict.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="房源标签" prop="tags">
          <el-input v-model="form.tags" placeholder="请输入房源标签"/>
        </el-form-item>
        <el-form-item label="产权性质" prop="propertyRightType">
          <el-select v-model="form.propertyRightType" placeholder="请选择产权性质">
            <el-option
              v-for="dict in dict.type.house_property_right_type"
              :key="dict.value"
              :label="dict.label"
              :value="dict.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="产权年限" prop="propertyRightYear">
          <el-select v-model="form.propertyRightYear" placeholder="请选择产权年限">
            <el-option
              v-for="dict in dict.type.house_property_right_year"
              :key="dict.value"
              :label="dict.label"
              :value="dict.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="房源介绍" prop="houseIntro">
          <el-input v-model="form.houseIntro" placeholder="请输入房源介绍"/>
        </el-form-item>
        <el-form-item label="房源图片" prop="imageUrls">
          <image-upload separator=";" v-model="form.imageUrls"/>
        </el-form-item>
        <el-form-item label="物业类型" prop="propertyType">
          <el-select v-model="form.propertyType" placeholder="请选择物业类型">
            <el-option
              v-for="dict in dict.type.house_property_type"
              :key="dict.value"
              :label="dict.label"
              :value="dict.value"
            ></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitForm">确 定</el-button>
        <el-button @click="cancel">取 消</el-button>
      </div>
    </el-dialog>

    <!-- 导入对话框 -->
    <el-dialog :title="upload.title" :visible.sync="upload.open" width="400px" append-to-body>
      <el-upload
        ref="upload"
        :limit="1"
        accept=".xlsx, .xls"
        :headers="upload.headers"
        :action="upload.url"
        :disabled="upload.isUploading"
        :on-progress="handleFileUploadProgress"
        :on-success="handleFileSuccess"
        :auto-upload="false"
        drag
      >
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
        <div class="el-upload__tip text-center" slot="tip">
          <span>仅允许导入xls、xlsx格式文件。</span>
          <el-link type="primary" :underline="false" style="font-size:12px;vertical-align: baseline;"
                   @click="importTemplate">下载模板
          </el-link>
        </div>
      </el-upload>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitFileForm">确 定</el-button>
        <el-button @click="upload.open = false">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>


import {addHouse, delHouse, getHouse, listHouse, updateHouse} from "@/api/house/house";
import {getToken} from "@/utils/auth";

export default {
  name: "House",
  dicts: ['house_city', 'house_town', 'house_orientation', 'house_floor_type', 'house_decoration_type', 'house_property_right_type', 'house_property_type', 'house_property_right_year', 'house_type'],
  data() {
    return {
      //是否是更新
      isUpdate: false,
      // 遮罩层
      loading: true,
      // 选中数组
      ids: [],
      // 非单个禁用
      single: true,
      // 非多个禁用
      multiple: true,
      // 显示搜索条件
      showSearch: true,
      // 总条数
      total: 0,
      // 房源信息表格数据
      houseList: [],
      // 表格列信息
      columns: [
        {key: 0, label: '房源编号', visible: false},
        {key: 1, label: '房源编码', visible: false},
        {key: 2, label: '封面图片', visible: true},
        {key: 3, label: '房源标题', visible: true},
        {key: 4, label: '小区名称', visible: true},
        {key: 5, label: '小区地址', visible: false},
        {key: 6, label: '所属区域', visible: true},
        {key: 7, label: '城市', visible: false},
        {key: 8, label: '镇', visible: false},
        {key: 9, label: '总价', visible: true},
        {key: 10, label: '单价', visible: true},
        {key: 11, label: '户型', visible: true},
        {key: 12, label: '建筑面积', visible: true},
        {key: 13, label: '朝向', visible: true},
        {key: 14, label: '楼层', visible: true},
        {key: 15, label: '楼层高度', visible: false},
        {key: 16, label: '装修面积单价', visible: false},
        {key: 17, label: '楼层类型', visible: false},
        {key: 18, label: '建筑年代', visible: true},
        {key: 19, label: '装修类型', visible: true},
        {key: 20, label: '房源标签', visible: true},
        {key: 21, label: '产权性质', visible: true},
        {key: 22, label: '产权年限', visible: true},
        {key: 23, label: '房源介绍', visible: false},
        {key: 24, label: '房源图片', visible: false},
        {key: 25, label: '物业类型', visible: true}
      ],
      // 弹出层标题
      title: "",
      // 是否显示弹出层
      open: false,
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        houseId: null,
        houseCode: null,
        title: null,
        community: null,
        city: null,
        town: null,
        houseType: null,
        orientation: null,
        floorHeight: null,
        floorType: null,
        buildingYear: null,
        decorationType: null,
        tags: null,
        propertyRightType: null,
        propertyRightYear: null,
        propertyType: null
      },
      // 表单参数
      form: {},
      // 导入参数
      upload: {
        // 是否显示弹出层（导入）
        open: false,
        // 弹出层标题（导入）
        title: "",
        // 是否禁用上传
        isUploading: false,
        // 设置上传的请求头部
        headers: {Authorization: "Bearer " + getToken()},
        // 上传的地址
        url: process.env.VUE_APP_BASE_API + "/house/house/importData"
      },
      // 表单校验
      rules: {
        houseId: [
          {required: true, message: "房源编号不能为空", trigger: "blur"}
        ],
        houseCode: [
          {required: true, message: "房源编码不能为空", trigger: "blur"}
        ]
      }
    };
  },
  created() {
    this.getList();
  },
  methods: {
    /** 查询房源信息列表 */
    getList() {
      this.loading = true;
      listHouse(this.queryParams).then(response => {
        this.houseList = response.rows;
        this.total = response.total;
        this.loading = false;
      });
    },
    // 取消按钮
    cancel() {
      this.open = false;
      this.reset();
    },
    // 表单重置
    reset() {
      this.form = {
        houseId: null,
        houseCode: null,
        coverImage: null,
        title: null,
        community: null,
        address: null,
        area: null,
        city: null,
        town: null,
        totalPrice: null,
        unitPrice: null,
        houseType: null,
        areaSize: null,
        orientation: null,
        floor: null,
        floorHeight: null,
        decorationArea: null,
        floorType: null,
        buildingYear: null,
        decorationType: null,
        tags: null,
        propertyRightType: null,
        propertyRightYear: null,
        houseIntro: null,
        imageUrls: null,
        propertyType: null
      };
      this.resetForm("form");
      this.isUpdate = false;
    },
    /** 搜索按钮操作 */
    handleQuery() {
      this.queryParams.pageNum = 1;
      this.getList();
    },
    /** 重置按钮操作 */
    resetQuery() {
      this.resetForm("queryForm");
      this.handleQuery();
    },
    // 多选框选中数据
    handleSelectionChange(selection) {
      this.ids = selection.map(item => item.houseId)
      this.single = selection.length !== 1
      this.multiple = !selection.length
    },
    /** 新增按钮操作 */
    handleAdd() {
      this.reset();
      this.open = true;
      this.title = "添加房源信息";
    },
    /** 修改按钮操作 */
    handleUpdate(row) {
      this.reset();
      const houseId = row.houseId || this.ids
      this.isUpdate = true;
      getHouse(houseId).then(response => {
        this.form = response.data;
        this.open = true;
        this.title = "修改房源信息";
      });
    },
    /** 提交按钮 */
    submitForm() {
      this.$refs["form"].validate(valid => {
        if (valid) {
          const submitData = this.buildSubmitData();
          if (submitData.houseId != null && this.isUpdate) {
            updateHouse(submitData).then(response => {
              this.$modal.msgSuccess("修改成功");
              this.open = false;
              this.getList();
            });
          } else {
            addHouse(submitData).then(response => {
              this.$modal.msgSuccess("新增成功");
              this.open = false;
              this.getList();
            });
          }
        }
      });
    },
    /** 删除按钮操作 */
    handleDelete(row) {
      const houseIds = row.houseId || this.ids;
      this.$modal.confirm('是否确认删除房源信息编号为"' + houseIds + '"的数据项？').then(function () {
        return delHouse(houseIds);
      }).then(() => {
        this.getList();
        this.$modal.msgSuccess("删除成功");
      }).catch(() => {
      });
    },
    /** 导出按钮操作 */
    handleExport() {
      this.download('house/house/export', {
        ...this.queryParams
      }, `house_${new Date().getTime()}.xlsx`)
    },
    /** 导入按钮操作 */
    handleImport() {
      this.upload.title = "房源信息导入";
      this.upload.open = true;
    },
    /** 下载模板操作 */
    importTemplate() {
      this.download(
        "house/house/importTemplate",
        {},
        "house_template_" + new Date().getTime() + ".xlsx"
      );
    },
    // 文件上传中处理
    handleFileUploadProgress(event, file, fileList) {
      this.upload.isUploading = true;
    },
    // 文件上传成功处理
    handleFileSuccess(response, file, fileList) {
      this.upload.open = false;
      this.upload.isUploading = false;
      this.$refs.upload.clearFiles();
      this.$alert("<div style='overflow: auto;overflow-x: hidden;max-height: 70vh;padding: 10px 20px 0;'>" + response.msg + "</div>", "导入结果", {dangerouslyUseHTMLString: true});
      this.$modal.closeLoading()
      this.getList();
    },
    buildSubmitData() {
      const data = {...this.form};
      if (data.totalPrice !== null && data.totalPrice !== undefined && data.totalPrice !== "") {
        data.totalPrice = parseFloat(data.totalPrice);
      } else {
        data.totalPrice = null;
      }
      if (data.unitPrice !== null && data.unitPrice !== undefined && data.unitPrice !== "") {
        data.unitPrice = parseFloat(data.unitPrice);
      } else {
        data.unitPrice = null;
      }
      if (data.areaSize !== null && data.areaSize !== undefined && data.areaSize !== "") {
        data.areaSize = parseInt(data.areaSize, 10);
      } else {
        data.areaSize = null;
      }
      if (data.floorHeight !== null && data.floorHeight !== undefined && data.floorHeight !== "") {
        data.floorHeight = parseInt(data.floorHeight, 10);
      } else {
        data.floorHeight = null;
      }
      if (data.decorationArea !== null && data.decorationArea !== undefined && data.decorationArea !== "") {
        data.decorationArea = parseFloat(data.decorationArea);
      } else {
        data.decorationArea = null;
      }
      if (data.buildingYear !== null && data.buildingYear !== undefined && data.buildingYear !== "") {
        data.buildingYear = parseInt(data.buildingYear, 10);
      } else {
        data.buildingYear = null;
      }
      return data;
    },
    // 提交上传文件
    submitFileForm() {
      this.$modal.loading("导入中请稍后")
      this.$refs.upload.submit();
    }
  }
};
</script>
