CREATE EXTERNAL TABLE `valorant_match_resume`(
    `result` ARRAY<
        STRUCT<
            `match_page`: STRING
            ,`team1`: STRING
            ,`team2`: STRING
            ,`score1`: STRING
            ,`score2`: STRING
            ,`tournament_name`: STRING
            ,`round_info`: STRING
        >
    >
)
PARTITIONED BY (`dt` STRING)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe' 
STORED AS INPUTFORMAT 'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION's3://esport-raw-bucket/game=valorant/content=match_resume/'
TBLPROPERTIES ('classification'='json')