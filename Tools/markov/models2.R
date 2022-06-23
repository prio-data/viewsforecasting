


## Test, calibration, and training periods

# train_w_calib <- 121:408
# calib <- 409:444
# train_w_test <- 121:444
# test <- 445:480
# train_real <- 121:488
# test_real <- 490:495

################################################################################
# FEATURE TRANSFORM COLSETS
################################################################################


#  conflict_dummies
  conflict_dummies<-c(
"ged_dummy_sb",
"ged_dummy_ns",
"ged_dummy_os")

#  time_since_best_5
  time_since_best_5<-c(
"time_since_greq_5_ged_best_sb",
"time_since_greq_5_ged_best_ns",
"time_since_greq_5_ged_best_os")

#  time_since_greq_25_ged_best_sb_ns_os
  time_since_greq_25_ged_best_sb_ns_os<-c(
"time_since_greq_25_ged_best_sb",
"time_since_greq_25_ged_best_ns",
"time_since_greq_25_ged_best_os")

#  time_since_best_100
  time_since_best_100<-c(
"time_since_greq_100_ged_best_sb",
"time_since_greq_100_ged_best_ns",
"time_since_greq_100_ged_best_os")

#  time_since_greq_500_ged_best_sb_ns_os
  time_since_greq_500_ged_best_sb_ns_os<-c(
"time_since_greq_500_ged_best_sb",
"time_since_greq_500_ged_best_ns",
"time_since_greq_500_ged_best_os")

#  tlags_1_to_12_greq_1_ged_best_sb
  tlags_1_to_12_greq_1_ged_best_sb<-c(
"tlag_1_greq_1_ged_best_sb",
"tlag_2_greq_1_ged_best_sb",
"tlag_3_greq_1_ged_best_sb",
"tlag_4_greq_1_ged_best_sb",
"tlag_5_greq_1_ged_best_sb",
"tlag_6_greq_1_ged_best_sb",
"tlag_7_greq_1_ged_best_sb",
"tlag_8_greq_1_ged_best_sb",
"tlag_9_greq_1_ged_best_sb",
"tlag_10_greq_1_ged_best_sb",
"tlag_11_greq_1_ged_best_sb",
"tlag_12_greq_1_ged_best_sb")

#  tlags_1_to_12_greq_5_ged_best_sb
  tlags_1_to_12_greq_5_ged_best_sb<-c(
"tlag_1_greq_5_ged_best_sb",
"tlag_2_greq_5_ged_best_sb",
"tlag_3_greq_5_ged_best_sb",
"tlag_4_greq_5_ged_best_sb",
"tlag_5_greq_5_ged_best_sb",
"tlag_6_greq_5_ged_best_sb",
"tlag_7_greq_5_ged_best_sb",
"tlag_8_greq_5_ged_best_sb",
"tlag_9_greq_5_ged_best_sb",
"tlag_10_greq_5_ged_best_sb",
"tlag_11_greq_5_ged_best_sb",
"tlag_12_greq_5_ged_best_sb")

#  tlags_1_to_12_greq_25_ged_best_sb
  tlags_1_to_12_greq_25_ged_best_sb<-c(
"tlag_1_greq_25_ged_best_sb",
"tlag_2_greq_25_ged_best_sb",
"tlag_3_greq_25_ged_best_sb",
"tlag_4_greq_25_ged_best_sb",
"tlag_5_greq_25_ged_best_sb",
"tlag_6_greq_25_ged_best_sb",
"tlag_7_greq_25_ged_best_sb",
"tlag_8_greq_25_ged_best_sb",
"tlag_9_greq_25_ged_best_sb",
"tlag_10_greq_25_ged_best_sb",
"tlag_11_greq_25_ged_best_sb",
"tlag_12_greq_25_ged_best_sb")

#  tlags_1_to_12_greq_100_ged_best_sb
  tlags_1_to_12_greq_100_ged_best_sb<-c(
"tlag_1_greq_100_ged_best_sb",
"tlag_2_greq_100_ged_best_sb",
"tlag_3_greq_100_ged_best_sb",
"tlag_4_greq_100_ged_best_sb",
"tlag_5_greq_100_ged_best_sb",
"tlag_6_greq_100_ged_best_sb",
"tlag_7_greq_100_ged_best_sb",
"tlag_8_greq_100_ged_best_sb",
"tlag_9_greq_100_ged_best_sb",
"tlag_10_greq_100_ged_best_sb",
"tlag_11_greq_100_ged_best_sb",
"tlag_12_greq_100_ged_best_sb")

#  tlags_1_to_12_greq_500_ged_best_sb
  tlags_1_to_12_greq_500_ged_best_sb<-c(
"tlag_1_greq_500_ged_best_sb",
"tlag_2_greq_500_ged_best_sb",
"tlag_3_greq_500_ged_best_sb",
"tlag_4_greq_500_ged_best_sb",
"tlag_5_greq_500_ged_best_sb",
"tlag_6_greq_500_ged_best_sb",
"tlag_7_greq_500_ged_best_sb",
"tlag_8_greq_500_ged_best_sb",
"tlag_9_greq_500_ged_best_sb",
"tlag_10_greq_500_ged_best_sb",
"tlag_11_greq_500_ged_best_sb",
"tlag_12_greq_500_ged_best_sb")

#  tlags_1_to_12_greq_1_ged_best_ns
  tlags_1_to_12_greq_1_ged_best_ns<-c(
"tlag_1_greq_1_ged_best_ns",
"tlag_2_greq_1_ged_best_ns",
"tlag_3_greq_1_ged_best_ns",
"tlag_4_greq_1_ged_best_ns",
"tlag_5_greq_1_ged_best_ns",
"tlag_6_greq_1_ged_best_ns",
"tlag_7_greq_1_ged_best_ns",
"tlag_8_greq_1_ged_best_ns",
"tlag_9_greq_1_ged_best_ns",
"tlag_10_greq_1_ged_best_ns",
"tlag_11_greq_1_ged_best_ns",
"tlag_12_greq_1_ged_best_ns")

#  tlags_1_to_12_greq_5_ged_best_ns
  tlags_1_to_12_greq_5_ged_best_ns<-c(
"tlag_1_greq_5_ged_best_ns",
"tlag_2_greq_5_ged_best_ns",
"tlag_3_greq_5_ged_best_ns",
"tlag_4_greq_5_ged_best_ns",
"tlag_5_greq_5_ged_best_ns",
"tlag_6_greq_5_ged_best_ns",
"tlag_7_greq_5_ged_best_ns",
"tlag_8_greq_5_ged_best_ns",
"tlag_9_greq_5_ged_best_ns",
"tlag_10_greq_5_ged_best_ns",
"tlag_11_greq_5_ged_best_ns",
"tlag_12_greq_5_ged_best_ns")

#  tlags_1_to_12_greq_25_ged_best_ns
  tlags_1_to_12_greq_25_ged_best_ns<-c(
"tlag_1_greq_25_ged_best_ns",
"tlag_2_greq_25_ged_best_ns",
"tlag_3_greq_25_ged_best_ns",
"tlag_4_greq_25_ged_best_ns",
"tlag_5_greq_25_ged_best_ns",
"tlag_6_greq_25_ged_best_ns",
"tlag_7_greq_25_ged_best_ns",
"tlag_8_greq_25_ged_best_ns",
"tlag_9_greq_25_ged_best_ns",
"tlag_10_greq_25_ged_best_ns",
"tlag_11_greq_25_ged_best_ns",
"tlag_12_greq_25_ged_best_ns")

#  tlags_1_to_12_greq_100_ged_best_ns
  tlags_1_to_12_greq_100_ged_best_ns<-c(
"tlag_1_greq_100_ged_best_ns",
"tlag_2_greq_100_ged_best_ns",
"tlag_3_greq_100_ged_best_ns",
"tlag_4_greq_100_ged_best_ns",
"tlag_5_greq_100_ged_best_ns",
"tlag_6_greq_100_ged_best_ns",
"tlag_7_greq_100_ged_best_ns",
"tlag_8_greq_100_ged_best_ns",
"tlag_9_greq_100_ged_best_ns",
"tlag_10_greq_100_ged_best_ns",
"tlag_11_greq_100_ged_best_ns",
"tlag_12_greq_100_ged_best_ns")

#  tlags_1_to_12_greq_500_ged_best_ns
  tlags_1_to_12_greq_500_ged_best_ns<-c(
"tlag_1_greq_500_ged_best_ns",
"tlag_2_greq_500_ged_best_ns",
"tlag_3_greq_500_ged_best_ns",
"tlag_4_greq_500_ged_best_ns",
"tlag_5_greq_500_ged_best_ns",
"tlag_6_greq_500_ged_best_ns",
"tlag_7_greq_500_ged_best_ns",
"tlag_8_greq_500_ged_best_ns",
"tlag_9_greq_500_ged_best_ns",
"tlag_10_greq_500_ged_best_ns",
"tlag_11_greq_500_ged_best_ns",
"tlag_12_greq_500_ged_best_ns")

#  tlags_1_to_12_greq_1_ged_best_os
  tlags_1_to_12_greq_1_ged_best_os<-c(
"tlag_1_greq_1_ged_best_os",
"tlag_2_greq_1_ged_best_os",
"tlag_3_greq_1_ged_best_os",
"tlag_4_greq_1_ged_best_os",
"tlag_5_greq_1_ged_best_os",
"tlag_6_greq_1_ged_best_os",
"tlag_7_greq_1_ged_best_os",
"tlag_8_greq_1_ged_best_os",
"tlag_9_greq_1_ged_best_os",
"tlag_10_greq_1_ged_best_os",
"tlag_11_greq_1_ged_best_os",
"tlag_12_greq_1_ged_best_os")

#  tlags_1_to_12_greq_5_ged_best_os
  tlags_1_to_12_greq_5_ged_best_os<-c(
"tlag_1_greq_5_ged_best_os",
"tlag_2_greq_5_ged_best_os",
"tlag_3_greq_5_ged_best_os",
"tlag_4_greq_5_ged_best_os",
"tlag_5_greq_5_ged_best_os",
"tlag_6_greq_5_ged_best_os",
"tlag_7_greq_5_ged_best_os",
"tlag_8_greq_5_ged_best_os",
"tlag_9_greq_5_ged_best_os",
"tlag_10_greq_5_ged_best_os",
"tlag_11_greq_5_ged_best_os",
"tlag_12_greq_5_ged_best_os")

#  tlags_1_to_12_greq_25_ged_best_os
  tlags_1_to_12_greq_25_ged_best_os<-c(
"tlag_1_greq_25_ged_best_os",
"tlag_2_greq_25_ged_best_os",
"tlag_3_greq_25_ged_best_os",
"tlag_4_greq_25_ged_best_os",
"tlag_5_greq_25_ged_best_os",
"tlag_6_greq_25_ged_best_os",
"tlag_7_greq_25_ged_best_os",
"tlag_8_greq_25_ged_best_os",
"tlag_9_greq_25_ged_best_os",
"tlag_10_greq_25_ged_best_os",
"tlag_11_greq_25_ged_best_os",
"tlag_12_greq_25_ged_best_os")

#  tlags_1_to_12_greq_100_ged_best_os
  tlags_1_to_12_greq_100_ged_best_os<-c(
"tlag_1_greq_100_ged_best_os",
"tlag_2_greq_100_ged_best_os",
"tlag_3_greq_100_ged_best_os",
"tlag_4_greq_100_ged_best_os",
"tlag_5_greq_100_ged_best_os",
"tlag_6_greq_100_ged_best_os",
"tlag_7_greq_100_ged_best_os",
"tlag_8_greq_100_ged_best_os",
"tlag_9_greq_100_ged_best_os",
"tlag_10_greq_100_ged_best_os",
"tlag_11_greq_100_ged_best_os",
"tlag_12_greq_100_ged_best_os")

#  tlags_1_to_12_greq_500_ged_best_os
  tlags_1_to_12_greq_500_ged_best_os<-c(
"tlag_1_greq_500_ged_best_os",
"tlag_2_greq_500_ged_best_os",
"tlag_3_greq_500_ged_best_os",
"tlag_4_greq_500_ged_best_os",
"tlag_5_greq_500_ged_best_os",
"tlag_6_greq_500_ged_best_os",
"tlag_7_greq_500_ged_best_os",
"tlag_8_greq_500_ged_best_os",
"tlag_9_greq_500_ged_best_os",
"tlag_10_greq_500_ged_best_os",
"tlag_11_greq_500_ged_best_os",
"tlag_12_greq_500_ged_best_os")

#  tlags_1_to_12_greq_1_to_500_ged_best_sb
  tlags_1_to_12_greq_1_to_500_ged_best_sb<-c(
tlags_1_to_12_greq_1_ged_best_sb,
tlags_1_to_12_greq_5_ged_best_sb,
tlags_1_to_12_greq_25_ged_best_sb,
tlags_1_to_12_greq_100_ged_best_sb,
tlags_1_to_12_greq_500_ged_best_sb)

#  tlags_1_to_12_greq_1_to_500_ged_best_ns
  tlags_1_to_12_greq_1_to_500_ged_best_ns<-c(
tlags_1_to_12_greq_1_ged_best_ns,
tlags_1_to_12_greq_5_ged_best_ns,
tlags_1_to_12_greq_25_ged_best_ns,
tlags_1_to_12_greq_100_ged_best_ns,
tlags_1_to_12_greq_500_ged_best_ns)

#  tlags_1_to_12_greq_1_to_500_ged_best_os
  tlags_1_to_12_greq_1_to_500_ged_best_os<-c(
tlags_1_to_12_greq_1_ged_best_os,
tlags_1_to_12_greq_5_ged_best_os,
tlags_1_to_12_greq_25_ged_best_os,
tlags_1_to_12_greq_100_ged_best_os,
tlags_1_to_12_greq_500_ged_best_os)

#  tlags_1_to_12_greq_1_to_500_ged_best_sb_ns_os
  tlags_1_to_12_greq_1_to_500_ged_best_sb_ns_os<-c(
tlags_1_to_12_greq_1_to_500_ged_best_sb,
tlags_1_to_12_greq_1_to_500_ged_best_ns,
tlags_1_to_12_greq_1_to_500_ged_best_os)

#  tlag_1_greq_1_ged_best_sb_ns_os
  tlag_1_greq_1_ged_best_sb_ns_os<-c(
"tlag_1_greq_1_ged_best_sb",
"tlag_1_greq_1_ged_best_ns",
"tlag_1_greq_1_ged_best_os")

#  tlag_2_to_3_greq_1_ged_best_sb
  tlag_2_to_3_greq_1_ged_best_sb<-c(
"tlag_2_greq_1_ged_best_sb",
"tlag_3_greq_1_ged_best_sb")

#  time_since_ged_dummy_sb_ns_os
  time_since_ged_dummy_sb_ns_os<-c(
"time_since_ged_dummy_sb",
"time_since_ged_dummy_ns",
"time_since_ged_dummy_os")

#  time_since_splag_1_1_ged_dummy_sb_ns_os
  time_since_splag_1_1_ged_dummy_sb_ns_os<-c(
"time_since_splag_1_1_ged_dummy_sb",
"time_since_splag_1_1_ged_dummy_ns",
"time_since_splag_1_1_ged_dummy_os")

#  time_since_acled_dummy_sb_ns_os
  time_since_acled_dummy_sb_ns_os<-c(
"time_since_acled_dummy_sb",
"time_since_acled_dummy_ns",
"time_since_acled_dummy_os")

#  time_since_greq_5_to_500_ged_best_sb_ns_os
  time_since_greq_5_to_500_ged_best_sb_ns_os<-c(
"time_since_greq_5_ged_best_sb",
"time_since_greq_5_ged_best_ns",
"time_since_greq_5_ged_best_os",
"time_since_greq_25_ged_best_sb",
"time_since_greq_25_ged_best_ns",
"time_since_greq_25_ged_best_os",
"time_since_greq_100_ged_best_sb",
"time_since_greq_100_ged_best_ns",
"time_since_greq_100_ged_best_os",
"time_since_greq_500_ged_best_sb",
"time_since_greq_500_ged_best_ns",
"time_since_greq_500_ged_best_os")

#  time_since_greq_5_to_500_splag_1_1_ged_best_sb_ns_os
  time_since_greq_5_to_500_splag_1_1_ged_best_sb_ns_os<-c(
"time_since_greq_5_splag_1_1_ged_best_sb",
"time_since_greq_5_splag_1_1_ged_best_ns",
"time_since_greq_5_splag_1_1_ged_best_os",
"time_since_greq_25_splag_1_1_ged_best_sb",
"time_since_greq_25_splag_1_1_ged_best_ns",
"time_since_greq_25_splag_1_1_ged_best_os",
"time_since_greq_100_splag_1_1_ged_best_sb",
"time_since_greq_100_splag_1_1_ged_best_ns",
"time_since_greq_100_splag_1_1_ged_best_os",
"time_since_greq_500_splag_1_1_ged_best_sb",
"time_since_greq_500_splag_1_1_ged_best_ns",
"time_since_greq_500_splag_1_1_ged_best_os")

#  time_since_splag_1_1_acled_dummy_sb_ns_os
  time_since_splag_1_1_acled_dummy_sb_ns_os<-c(
"time_since_splag_1_1_acled_dummy_sb",
"time_since_splag_1_1_acled_dummy_ns",
"time_since_splag_1_1_acled_dummy_os")

#  time_since_greq_100_splag_1_1_ged_best_sb_ns_os
  time_since_greq_100_splag_1_1_ged_best_sb_ns_os<-c(
"time_since_greq_100_splag_1_1_ged_best_sb",
"time_since_greq_100_splag_1_1_ged_best_ns",
"time_since_greq_100_splag_1_1_ged_best_os")

#  splag_1_1_ged_best_sb_ns_os
  splag_1_1_ged_best_sb_ns_os<-c(
"splag_1_1_ged_best_sb",
"splag_1_1_ged_best_ns",
"splag_1_1_ged_best_os")

#  splag_1_1_tlag_1_ged_best_sb_ns_os
  splag_1_1_tlag_1_ged_best_sb_ns_os<-c(
"splag_1_1_tlag_1_ged_best_sb",
"splag_1_1_tlag_1_ged_best_ns",
"splag_1_1_tlag_1_ged_best_os")

#  splag_1_1_splag_1_1_acled_count_sb_ns_os
  splag_1_1_splag_1_1_acled_count_sb_ns_os<-c(
"splag_1_1_acled_count_sb",
"splag_1_1_acled_count_ns",
"splag_1_1_acled_count_os")

#  splag_1_1_acled_count_sb_ns_os
  splag_1_1_acled_count_sb_ns_os<-c(
"splag_1_1_acled_count_sb",
"splag_1_1_acled_count_ns",
"splag_1_1_acled_count_os")

#  fix
  fix<-c(
"time_since_greq_100_splag_1_1_ged_best_sb")

#  fix2
  fix2<-c(
"splag_1_1_ged_best_ns",
"splag_1_1_ged_best_os")

#  cdummies
  cdummies<-c(
"cdum_1",
"cdum_2",
"cdum_3",
"cdum_4",
"cdum_5",
"cdum_6",
"cdum_7",
"cdum_8",
"cdum_9",
"cdum_10",
"cdum_11",
"cdum_12",
"cdum_13",
"cdum_14",
"cdum_15",
"cdum_16",
"cdum_17",
"cdum_18",
"cdum_19",
"cdum_20",
"cdum_21",
"cdum_22",
"cdum_23",
"cdum_24",
"cdum_25",
"cdum_26",
"cdum_27",
"cdum_28",
"cdum_29",
"cdum_30",
"cdum_31",
"cdum_32",
"cdum_33",
"cdum_34",
"cdum_35",
"cdum_36",
"cdum_37",
"cdum_38",
"cdum_39",
"cdum_40",
"cdum_41",
"cdum_42",
"cdum_43",
"cdum_44",
"cdum_45",
"cdum_46",
"cdum_47",
"cdum_48",
"cdum_49",
"cdum_50",
"cdum_51",
"cdum_52",
"cdum_53",
"cdum_54",
"cdum_55",
"cdum_56",
"cdum_57",
"cdum_58",
"cdum_59",
"cdum_60",
"cdum_61",
"cdum_62",
"cdum_63",
"cdum_64",
"cdum_65",
"cdum_66",
"cdum_67",
"cdum_68",
"cdum_69",
"cdum_70",
"cdum_71",
"cdum_72",
"cdum_73",
"cdum_74",
"cdum_75",
"cdum_76",
"cdum_77",
"cdum_78",
"cdum_79",
"cdum_80",
"cdum_81",
"cdum_82",
"cdum_83",
"cdum_84",
"cdum_85",
"cdum_86",
"cdum_87",
"cdum_88",
"cdum_89",
"cdum_90",
"cdum_91",
"cdum_92",
"cdum_93",
"cdum_94",
"cdum_95",
"cdum_96",
"cdum_97",
"cdum_98",
"cdum_99",
"cdum_100",
"cdum_101",
"cdum_102",
"cdum_103",
"cdum_104",
"cdum_105",
"cdum_106",
"cdum_107",
"cdum_108",
"cdum_109",
"cdum_110",
"cdum_111",
"cdum_112",
"cdum_113",
"cdum_114",
"cdum_115",
"cdum_116",
"cdum_117",
"cdum_118",
"cdum_119",
"cdum_120",
"cdum_121",
"cdum_122",
"cdum_123",
"cdum_124",
"cdum_125",
"cdum_126",
"cdum_127",
"cdum_128",
"cdum_129",
"cdum_130",
"cdum_131",
"cdum_132",
"cdum_133",
"cdum_134",
"cdum_135",
"cdum_136",
"cdum_137",
"cdum_138",
"cdum_139",
"cdum_140",
"cdum_141",
"cdum_142",
"cdum_143",
"cdum_144",
"cdum_145",
"cdum_146",
"cdum_147",
"cdum_148",
"cdum_149",
"cdum_150",
"cdum_151",
"cdum_152",
"cdum_153",
"cdum_154",
"cdum_155",
"cdum_156",
"cdum_157",
"cdum_158",
"cdum_159",
"cdum_160",
"cdum_161",
"cdum_162",
"cdum_163",
"cdum_164",
"cdum_165",
"cdum_166",
"cdum_167",
"cdum_168",
"cdum_169",
"cdum_170",
"cdum_171",
"cdum_172",
"cdum_173",
"cdum_174",
"cdum_175",
"cdum_176",
"cdum_177",
"cdum_178",
"cdum_179",
"cdum_180",
"cdum_181",
"cdum_182",
"cdum_183",
"cdum_184",
"cdum_185",
"cdum_186",
"cdum_187",
"cdum_188",
"cdum_189",
"cdum_190",
"cdum_191",
"cdum_192",
"cdum_193",
"cdum_194",
"cdum_195",
"cdum_196",
"cdum_197",
"cdum_198",
"cdum_199",
"cdum_200",
"cdum_201",
"cdum_202",
"cdum_203",
"cdum_204",
"cdum_205",
"cdum_206",
"cdum_207",
"cdum_208",
"cdum_209",
"cdum_210",
"cdum_211",
"cdum_212",
"cdum_213",
"cdum_214",
"cdum_215",
"cdum_216",
"cdum_217",
"cdum_218",
"cdum_219",
"cdum_220",
"cdum_221",
"cdum_222",
"cdum_223",
"cdum_224",
"cdum_225",
"cdum_226",
"cdum_227",
"cdum_228",
"cdum_229",
"cdum_230",
"cdum_231",
"cdum_232",
"cdum_233",
"cdum_234",
"cdum_235",
"cdum_236",
"cdum_237",
"cdum_238",
"cdum_239",
"cdum_240",
"cdum_241",
"cdum_242",
"cdum_243",
"cdum_244",
"cdum_245",
"cdum_246",
"cdum_247",
"cdum_248",
"cdum_249",
"cdum_250",
"cdum_251",
"cdum_252",
"cdum_253",
"cdum_254",
"cdum_255")


################################################################################
# THEMES
################################################################################


#  acled_violence
  acled_violence <- c(
time_since_acled_dummy_sb_ns_os,
time_since_splag_1_1_acled_dummy_sb_ns_os,
splag_1_1_acled_count_sb_ns_os)

# acled_protest
  acled_protest <- c(
"time_since_acled_dummy_pr",
"splag_1_1_acled_count_pr",
"time_since_splag_1_1_acled_dummy_pr")

# base_ext
  base_ext <- c(
"fvp_grgdpcap_nonoilrent",
"fvp_grgdpcap_oilrent",
"fvp_lngdpcap_nonoilrent",
"fvp_lngdpcap_oilrent",
"fvp_population200",
"fvp_ssp2_edu_sec_15_24_prop",
"fvp_ssp2_urban_share_iiasa")

#  cfshort
  cfshort <- c(
splag_1_1_ged_best_sb_ns_os,
#splag_1_1_tlag_1_ged_best_sb_ns_os,
time_since_ged_dummy_sb_ns_os,
fix,
time_since_greq_25_ged_best_sb_ns_os,
time_since_greq_500_ged_best_sb_ns_os,
time_since_splag_1_1_ged_dummy_sb_ns_os,
tlag_1_greq_1_ged_best_sb_ns_os,
tlag_2_to_3_greq_1_ged_best_sb)

# cflong
  cflong <- c(
time_since_ged_dummy_sb_ns_os,
tlags_1_to_12_greq_1_to_500_ged_best_sb_ns_os,
time_since_greq_5_to_500_ged_best_sb_ns_os,
time_since_greq_5_to_500_splag_1_1_ged_best_sb_ns_os)

# confhist_2019
  confhist_2019 <- c(
tlags_1_to_12_greq_1_ged_best_sb,
time_since_ged_dummy_sb_ns_os,
fix2)

# demog
  demog <- c(
"fvp_population200",
"fvp_ssp2_edu_sec_15_24_prop",
"fvp_ssp2_urban_share_iiasa",
"fvp_grpop200",
"wdi_sp_dyn_imrt_in",
"wdi_sp_dyn_tfrt_in")

# demog_conf
  demog_conf <- c(
demog,
cfshort)

#econ:
econ <- c(
"wdi_ny_gdp_pcap_cd",
"wdi_ny_gdp_mktp_cd",
"fvp_grgdpcap_nonoilrent",
"fvp_grgdpcap_oilrent",
"fvp_lngdpcap_nonoilrent",
"fvp_lngdpcap_oilrent",
"fvp_lngdp200",
"fvp_lngdppercapita200")

# econ_conf
  econ_conf <- c(
econ,
cfshort)

# icgcw
  icgcw <- c(
"icgcw_alerts",
"icgcw_opportunities",
"icgcw_deteriorated",
"icgcw_improved",
"icgcw_unobserved")

# icgcw_conf
  icgcw_conf <- c(
icgcw,
cfshort)

# inst
  inst <- c(
"fvp_prop_excluded",
"fvp_semi",
"fvp_demo",
"fvp_timeindep",
"fvp_timesincepreindepwar",
"fvp_timesinceregimechange",
"fvp_prop_discriminated",
"fvp_prop_dominant",
"fvp_prop_irrelevant",
"fvp_prop_powerless",
"fvp_indepyear")

# inst_conf
  inst_conf <- c(
inst,
cfshort)

# neibhist
  neibhist <- c(
time_since_greq_5_to_500_splag_1_1_ged_best_sb_ns_os,
splag_1_1_ged_best_sb_ns_os,
#splag_1_1_tlag_1_ged_best_sb_ns_os,
time_since_splag_1_1_acled_dummy_sb_ns_os,
splag_1_1_splag_1_1_acled_count_sb_ns_os)

#  reign_base
  reign_base <- c(
"reign_age",
"reign_anticipation",
"reign_change_recent",
"reign_defeat_recent",
"reign_delayed",
"reign_direct_recent",
"reign_elected",
"reign_election_now",
"reign_election_recent",
"reign_exec_ant",
"reign_exec_recent",
"reign_gov_dominant_party",
"reign_gov_foreign_occupied",
"reign_gov_indirect_military",
"reign_gov_military",
"reign_gov_military_personal",
"reign_gov_monarchy",
"reign_gov_oligarchy",
"reign_gov_parliamentary_democracy",
"reign_gov_party_military",
"reign_gov_party_personal",
"reign_gov_party_personal_military_hybrid",
"reign_gov_personal_dictatorship",
"reign_gov_presidential_democracy",
"reign_gov_provisional_civilian",
"reign_gov_provisional_military",
"reign_gov_warlordism",
"reign_indirect_recent",
"reign_irreg_lead_ant",
"reign_irregular",
"reign_lastelection",
"reign_lead_recent",
"reign_leg_ant",
"reign_leg_recent",
"reign_loss",
"reign_male",
"reign_militarycareer",
"reign_nochange_recent",
"reign_prev_conflict",
"reign_pt_attempt",
"reign_pt_suc",
"reign_ref_ant",
"reign_ref_recent",
"reign_tenure_months",
"reign_victory_recent")

# reign_coups
  reign_coups <- c(
"reign_couprisk",
"reign_pctile_risk")

# reign_coups_conf
  reign_coups_conf <- c(
reign_coups,
cfshort)

# reign_drought
  reign_drought <- c(
"reign_precip")

# reign_drought_conf
  reign_drought_conf <- c(
reign_drought,
cfshort)

# reign_conf
  reign_conf <- c(
reign_base,
cfshort)

#  vdem
  vdem <- c(
"vdem_v2x_accountability",
"vdem_v2x_api",
"vdem_v2x_civlib",
"vdem_v2x_clphy",
"vdem_v2x_clpol",
"vdem_v2x_clpriv",
"vdem_v2x_corr",
"vdem_v2x_cspart",
"vdem_v2x_delibdem",
"vdem_v2x_diagacc",
"vdem_v2x_divparctrl",
"vdem_v2x_edcomp_thick",
"vdem_v2x_egal",
"vdem_v2x_egaldem",
"vdem_v2x_elecoff",
"vdem_v2x_elecreg",
"vdem_v2x_ex_confidence",
"vdem_v2x_ex_direlect",
"vdem_v2x_ex_hereditary",
"vdem_v2x_ex_military",
"vdem_v2x_ex_party",
"vdem_v2x_execorr",
"vdem_v2x_feduni",
"vdem_v2x_frassoc_thick",
"vdem_v2x_freexp",
"vdem_v2x_freexp_altinf",
"vdem_v2x_gencl",
"vdem_v2x_gencs",
"vdem_v2x_gender",
"vdem_v2x_genpp",
"vdem_v2x_horacc",
"vdem_v2x_hosabort",
"vdem_v2x_hosinter",
"vdem_v2x_jucon",
"vdem_v2x_legabort",
"vdem_v2x_libdem",
"vdem_v2x_liberal",
"vdem_v2x_mpi",
"vdem_v2x_neopat",
"vdem_v2x_partip",
"vdem_v2x_partipdem",
"vdem_v2x_polyarchy",
"vdem_v2x_pubcorr",
"vdem_v2x_regime",
"vdem_v2x_regime_amb",
"vdem_v2x_rule",
"vdem_v2x_suffr",
"vdem_v2x_veracc")

# vdem_conf
  vdem_conf <- c(
vdem,
cfshort)

# vdem_high
  vdem_high <- c(
"vdem_v2x_delibdem",
"vdem_v2x_egaldem",
"vdem_v2x_libdem",
"vdem_v2x_partipdem",
"vdem_v2x_polyarchy")

# all,
all <- c(
acled_violence,
acled_protest,
base_ext,
cfshort,
cflong,
confhist_2019,
demog,
demog_conf,
econ,
econ_conf,
icgcw,
icgcw_conf,
inst,
inst_conf,
neibhist,
reign_base,
reign_coups,
reign_coups_conf,
reign_drought,
reign_conf,
vdem,
vdem_conf,
vdem_high)

# allnew,
all2 <- c(
  acled_violence,
  acled_protest,
  base_ext,
  cfshort,
  cflong,
  confhist_2019,
  demog,
  demog_conf,
  econ,
  econ_conf,
  icgcw,
  icgcw_conf,
  inst,
  inst_conf,
  neibhist,
  reign_base,
  reign_coups,
  reign_coups_conf,
  reign_drought,
  reign_conf,
  vdem,
  vdem_conf,
  vdem_high)

all_list <- list(
  acled_violence,
  acled_protest,
  base_ext,
  cfshort,
  cflong,
  confhist_2019,
  demog,
  demog_conf,
  econ,
  econ_conf,
  icgcw,
  icgcw_conf,
  inst,
  inst_conf,
  neibhist,
  reign_base,
  reign_coups,
  reign_coups_conf,
  reign_drought,
  reign_conf,
  vdem,
  vdem_conf,
  vdem_high)

