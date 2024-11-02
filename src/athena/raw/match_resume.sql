CREATE EXTERNAL TABLE `match_resume`(
    `result` STRUCT<
        `match_page`: STRING
        ,`team1`: STRING
        ,`team2`: STRING
        ,`score1`: STRING
        ,`score2`: STRING
        ,`tournament_name`: STRING
        ,`round_info`: STRING
        ,`dat_load`: STRING
    >
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe' 
STORED AS INPUTFORMAT 'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION's3://esport-raw-bucket/game=valorant/'
TBLPROPERTIES ('classification'='json')