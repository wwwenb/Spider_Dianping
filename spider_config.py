
# 爬虫初始配置信息
class Config():

    def __init__(self):
        self.url = "http://www.dianping.com/hangzhou/ch10"

        # chrome
        # self.cookie = "fspop=test; _lxsdk_cuid=17a0969dff0c8-0388ad2d3cb4a6-f7f1939-100200-17a0969dff1c8; _hc.v=b3171166-89e9-cfd3-0f8e-a0095a8e05a1.1623655573; s_ViewType=10; cy=3; cye=hangzhou; ua=dpuser_6185476995; ctu=2a2e1c4a49e422ece1e1b02dd418c7bdf50c02237fddb9a24f10519d325bdd4b; cityid=7; default_ab=shopreviewlist:A:1; uuid=D4CD3F578C621AC0C97AE2C54B46C969411990BC9F962777CCF032333A6D6FBB; iuuid=D4CD3F578C621AC0C97AE2C54B46C969411990BC9F962777CCF032333A6D6FBB; _lxsdk=D4CD3F578C621AC0C97AE2C54B46C969411990BC9F962777CCF032333A6D6FBB; _ga=GA1.2.570212981.1623985393; dplet=7b726db2fc4478d77327421678eb5e74; dper=c0f11e2ea064e9dae1103763a4c8446659960d2afef26c88d84d44d456b16e190682524a3230c681ab7cdc2f2b1112bd0647f2e6b9616ea6e5b4750b4984878c11750a7546f534f1f2a2f7c58e85d52e6b602f15a72f2c3e9be68edf23908706; ll=7fd06e815b796be3df069dec7836c3df; _lx_utm=utm_source=google&utm_medium=organic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1624070266,1624095737,1624101954,1624102009; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1624103876; _lxsdk_s=17a23e4227c-84c-345-f26||582"
        # self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"

        # edge
        self.cookie = "fspop=test; _lx_utm=utm_source=google&utm_medium=organic; _lxsdk_cuid=17a28738ed7c8-0457aed04d822e-7f697c63-100200-17a28738ed8c8; _lxsdk=17a28738ed7c8-0457aed04d822e-7f697c63-100200-17a28738ed8c8; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1624176301; _hc.v=a3670bb9-0314-43fd-3c93-6d5c95515321.1624176301; dplet=6f7a62204bdf3dde537b04c2c21e5ed3; dper=bc4164eba9d3980da9fda94fe6b6adb71ac5337b962ef9a1852917c208e6a39d7762933e517c38290a0a7c8cdb88840c0542fabfa2d2584cb817dd904d54b2c0bdb53933aa9cfae3adcd1130a6e6a05875643d84eda146c1ae14cea0441c225f; ll=7fd06e815b796be3df069dec7836c3df; ua=dpuser_0399708362; ctu=6167c0aaf145930081bb90539118d82da9f3cd8bf102e50c0ef7e0dabc665207; uamo=15889371400; s_ViewType=10; cy=3; cye=hangzhou; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1624176461; _lxsdk_s=17a28738eda-9c7-de0-6a6||430"
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36 Edg/91.0.864.48"

        self.host = "www.dianping.com"
        self.year_limit = 2020

        self.result_file = "./result.csv"
        self.shopid_file = "./tmp/shop_id.txt"


spider_config = Config()