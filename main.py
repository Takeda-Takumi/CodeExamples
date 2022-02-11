import sys

# 深夜料金だったらtrueを返す関数
def isLateNight(cur_h, pre_h):
    cur_h_per24 = cur_h % 24  
    pre_h_per24 = pre_h % 24  
    
    if(((cur_h_per24 >= 0 and cur_h_per24 <= 4) or (cur_h_per24 >= 22 and cur_h_per24 <= 23)) and \
        ((pre_h_per24 >= 0 and pre_h_per24 <= 4) or (pre_h_per24 >= 22 and pre_h_per24 <= 23))):
        return True
    else:
        return False


def main(lines):
    # 定数
    INITIAL_FARE_DISTANCE_M    = 1052    #初乗料金になる距離
    INITIAL_FARE               = 410     #初乗料金
    ADDITIONAL_FARE            = 80      #初乗距離以降にかかる規定距離ごとの加算料金
    ADDITIONAL_FARE_DISTANCE_M = 237     #初乗距離以降にかかる料金がかかる距離
    SLOW_PACE_FARE_MPERH       = 10000   #低速運賃がかかる最高速度 meter/hour
    SLOW_PACE_FARE             = 80      #低速走行した距離に応じてかかる低速運賃
    SLOW_PACE_FARE_SEC         = 90      #低速運賃がかかる時間

    total_mileage_m = 0
    total_taxi_fare = INITIAL_FARE  #taxiに乗ったら絶対お金が掛かるので初乗り料金を初期値としているが、時間が1秒も進んでいないデータを渡されると乗っていないのに初乗り料金が掛かるバグが起こる
    total_slowspeed_time = 0

    for i in range(1, len(lines)):  #現在の注目している時刻とその一つ前の時刻について調べるので、添え字を1から始めている
        current_time_hour, current_time_minute, current_time_second = \
            map(float, lines[i].split()[0].split(":"))  #secが小数で与えられるのでintではなくfloatにしてます
        pre_time_hour, pre_time_minute, pre_time_second = \
            map(float, lines[i-1].split()[0].split(":"))
            
        current_mileage_m = float(lines[i].split()[1])

        time_difference_sec = \
            (current_time_hour - pre_time_hour)*(60*60) + (current_time_minute - pre_time_minute)*60 + (current_time_second - pre_time_second)

        #深夜だったら走行距離と走行時間を1.25倍にする
        if(isLateNight(current_time_hour, pre_time_hour)):
            total_mileage_m += (current_mileage_m * 1.25)
            time_difference_sec *= 1.25
        else:
            total_mileage_m += current_mileage_m

        current_velocity_mperh = current_mileage_m / (time_difference_sec / (60*60))

        #fix 低速だったら低速走行していた時間を
        if(current_velocity_mperh <= SLOW_PACE_FARE_MPERH):
            total_slowspeed_time += time_difference_sec

    #低速走行していた時間に応じて、低速運賃を加算する
    total_taxi_fare += (total_slowspeed_time // SLOW_PACE_FARE_SEC) * SLOW_PACE_FARE

    #初乗り距離以降の加算料金を求める
    if(total_mileage_m > INITIAL_FARE_DISTANCE_M):
        total_taxi_fare += ((total_mileage_m - INITIAL_FARE_DISTANCE_M) // ADDITIONAL_FARE_DISTANCE_M + 1) * ADDITIONAL_FARE #この条件分岐に来ている時点で, 初乗り距離は必ず超えているので+1をしてある
    print(int(total_taxi_fare))


if __name__ == '__main__':
    lines = []
    for l in sys.stdin:
        lines.append(l.rstrip('\r\n'))
    main(lines)
