# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: metrics_msg.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11metrics_msg.proto\x12\x07Metrics\"\x7f\n\x0c\x43PUDistFloat\x12;\n\x0brange2usecs\x18\x01 \x03(\x0b\x32&.Metrics.CPUDistFloat.Range2usecsEntry\x1a\x32\n\x10Range2usecsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x02:\x02\x38\x01\"\x81\x01\n\rCPUDistUint32\x12<\n\x0brange2usecs\x18\x01 \x03(\x0b\x32\'.Metrics.CPUDistUint32.Range2usecsEntry\x1a\x32\n\x10Range2usecsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\r:\x02\x38\x01\"M\n\x15MultipleCPUDistUint32\x12\x34\n\x14multiple_range2usecs\x18\x01 \x03(\x0b\x32\x16.Metrics.CPUDistUint32\"4\n\x0eMetricsRequest\x12\x0f\n\x07metrics\x18\x01 \x01(\t\x12\x11\n\tnode_name\x18\x02 \x01(\t\"\x8f\x01\n\x0fMetricsResponse\x12&\n\x07\x63pu_avg\x18\x01 \x01(\x0b\x32\x15.Metrics.CPUDistFloat\x12\'\n\x07\x63pu_sum\x18\x02 \x01(\x0b\x32\x16.Metrics.CPUDistUint32\x12+\n\x03\x63pu\x18\x03 \x01(\x0b\x32\x1e.Metrics.MultipleCPUDistUint322S\n\x0cQueryManager\x12\x43\n\x0cQueryMetrics\x12\x17.Metrics.MetricsRequest\x1a\x18.Metrics.MetricsResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'metrics_msg_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CPUDISTFLOAT_RANGE2USECSENTRY._options = None
  _CPUDISTFLOAT_RANGE2USECSENTRY._serialized_options = b'8\001'
  _CPUDISTUINT32_RANGE2USECSENTRY._options = None
  _CPUDISTUINT32_RANGE2USECSENTRY._serialized_options = b'8\001'
  _CPUDISTFLOAT._serialized_start=30
  _CPUDISTFLOAT._serialized_end=157
  _CPUDISTFLOAT_RANGE2USECSENTRY._serialized_start=107
  _CPUDISTFLOAT_RANGE2USECSENTRY._serialized_end=157
  _CPUDISTUINT32._serialized_start=160
  _CPUDISTUINT32._serialized_end=289
  _CPUDISTUINT32_RANGE2USECSENTRY._serialized_start=239
  _CPUDISTUINT32_RANGE2USECSENTRY._serialized_end=289
  _MULTIPLECPUDISTUINT32._serialized_start=291
  _MULTIPLECPUDISTUINT32._serialized_end=368
  _METRICSREQUEST._serialized_start=370
  _METRICSREQUEST._serialized_end=422
  _METRICSRESPONSE._serialized_start=425
  _METRICSRESPONSE._serialized_end=568
  _QUERYMANAGER._serialized_start=570
  _QUERYMANAGER._serialized_end=653
# @@protoc_insertion_point(module_scope)
