import gpt_scene
import gpt_prompts
import gpt_check
import gpt_request
import gpt_get_bbox
import time
# scene = {'objects': ['jap', 'crepen', 'weep'], 'relationships': [('jap', 'on the bottom of', 'crepen'), ('crepen', 'on the left of', 'weep')]}
# bbox = {
#   "jap": [100, 206, 60, 100],
#   "crepen": [0, 117.76, 63.17, 88.24],
#   "weep": [163.17, 117.76, 83.33, 125]
# }
res = {}
cnt = 0
for i in range(100, 200):
    try:
        # 随机获取
        if cnt >= 5:
            break
        scene = gpt_scene.generate_random_scene()
        # print(scene)
        prompts = gpt_prompts.get_prompts(scene)
        # print(prompts)
        # 去请求gpt4
        response = gpt_request.send_request(prompts)
        # print(response)
        bbox = gpt_get_bbox.get_bbox(response)
        # print(bbox)
        r = gpt_check.check_bbox(scene, bbox)
        res[str(i)] = r
        print("round {} cnt {}: {}".format(str(i), str(cnt), str(r)))
        cnt += 1
        # break
    except:
        print("error!!!!!!!!")
        print("res: ", res)
        time.sleep(5)
print("finished!!!!!!!!")
print("res: ", res)
