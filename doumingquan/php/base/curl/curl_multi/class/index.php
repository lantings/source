<?php 

class MultiCurl
{
    /*@var array $config*/
    private $config = array();
    /*@var string $baseUrl*/
    private $baseUrl = '';
    /**
     * @todo: 设置基础路径
     */
    public function setBaseUrl($url = '')
    {
        $this->baseUrl = $url;
        return $this;
    }
    /**
     * @todo: 设置配置参数
     */
    public function setConfig($config = array())
    {
        $baseUrl = $this->baseUrl ? $this->baseUrl : '';
        foreach($config as $val){
            $this->config[] = array(
                'url' => $val['url']
            );
        }
        return $this;
    }
    /**
     * @todo: 获取查询结果
     */
    public function getRes()
    {
        //2.加入子curl 
        $ch_arr= array();
        $mh = curl_multi_init();
        foreach($this->config as $k=>$val){
        	$ch_arr[$k] = curl_init();
        	curl_setopt($ch_arr[$k], CURLOPT_URL, $val['url']);
        	if(isset($ch_arr[$k]['configs'])){
        		foreach($ch_arr[$k]['configs'] as $kconfig => $config){
        		    curl_setopt($ch_arr[$k], $kconfig, $config);	
        		}
        	}
            curl_setopt($ch_arr[$k], CURLOPT_HEADER, 0);
        	curl_multi_add_handle($mh,$ch_arr[$k]);
        }
        //3.执行curl
        $active = null;
        do {
            $mrc = curl_multi_exec($mh, $active);
        } while ($mrc == CURLM_CALL_MULTI_PERFORM);
        while ($active && $mrc == CURLM_OK) {
            if (curl_multi_select($mh) == -1) {
                usleep(100);
            }
            do {
                $mrc = curl_multi_exec($mh, $active);
            } while ($mrc == CURLM_CALL_MULTI_PERFORM);
        }
        //4.关闭子curl
        foreach($ch_arr as $val){
            curl_multi_remove_handle($mh, $val);
        }
        //5.关闭父curl
        curl_multi_close($mh);
        //6.获取执行结果
        foreach($ch_arr as $val){
        	$response[] = curl_multi_getcontent($val);
        }
        return $response;
    }
}

		// $start=microtime_float();
echo time();
        $multicurl = new MultiCurl();
        $baseurl = 'http://www.baidu.com';
        $curl_configs = array(
            array('url'=> 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET'),
            array('url'=> 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET')
        );
        $res = $multicurl->setBaseUrl($baseurl)->setConfig($curl_configs)->getRes();
        // $end=microtime_float();
        // echo "\n",$end-$start;
        var_dump($res);
echo time();

//https://blog.csdn.net/wujiangwei567/article/details/77026602 


 ?>
