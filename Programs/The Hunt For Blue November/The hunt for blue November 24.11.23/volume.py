def tgt_volume(tgt_speed,tgt_loudness,distance):
    tgt_volume = (1+(tgt_loudness*tgt_speed))/((distance**2))
    return tgt_volume