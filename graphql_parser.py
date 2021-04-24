import re
import json

def remove_line_break(gql_exp):
  return gql_exp.replace('\n', ' ')

def convert_var_dict_to_gql_exp(var_dict):
  def get_var_dict_key(map_value, var_key_list):
    if isinstance(map_value, dict):
      for k, v in map_value.items():
        var_key_list.append(k)
        if isinstance(v, dict):
          get_var_dict_key(v, var_key_list)
    elif isinstance(map_value, list):
      for v in map_value:
        get_var_dict_key(v, var_key_list)
    return var_key_list

  var_dict_string = str(var_dict)
  var_key_list = get_var_dict_key(var_dict, [])

  indexes = []
  begin = 0
  for key in var_key_list:
    idx = var_dict_string.find(key, begin)
    if idx == -1:
      print('---------- error ----------')
      print(var_dict_string)
      raise RuntimeError("error")
    
    begin = idx + len(key)
    indexes.append(idx-1)
    indexes.append(begin)

  for each in indexes:
    var_dict_string = var_dict_string[:each] + ' ' + var_dict_string[each+1:]
  return var_dict_string

def remove_gql_exp_query_and_variables(gql_exp):
  p = re.search(r'{"query":"(.+)","variables":({.*})}',gql_exp)
  if not p or len(p.groups()) != 2:
    print('---------- error ----------')
    print(p)
    print(gql_exp)
    raise RuntimeError('[error]: var_string or query_string not exist')

  query_string = p.group(1)
  var_string = p.group(2)

  new_var_json = {}
  var_json = json.loads(var_string)
  for key,value in var_json.items():
    new_var_json[f'${key}'] = convert_var_dict_to_gql_exp(value)
  for key, value in new_var_json.items():
    query_string = query_string.replace(key, value)

  doubel_quotes_str = query_string.replace("'","\"")
  return doubel_quotes_str

def lower_bool(gql_exp):
  return gql_exp.replace("True", "true").replace("False", "false")

def add_curly_brackets(gql_exp):
  if re.match(r'\s*query', gql_exp):
    return '{' + gql_exp + '}'
  return gql_exp

def graphql_parser(gql_exp):
  responsibility_chain = [remove_line_break, remove_gql_exp_query_and_variables, lower_bool, add_curly_brackets]

  for func in responsibility_chain:
    gql_exp = func(gql_exp)
  return gql_exp

if __name__ == "__main__":
  # gql_exp = '{"query":"{\n    buckets (\n      groupBy: $groupBy,\n      orderBy: $orderBy,\n      filter:  $filter\n    ) {\n      key,\n      projects(orderBy: $projectOrderBy, filterGroup:$projectFilterGroup) {\n        _D9zH44Nb\n_2KPs1eoM{\n        uuid\n        value\n        bgColor\n        color\n        defaultSelected\n      }\n_PnafUbJo{\n        uuid\n        value\n        bgColor\n        color\n        defaultSelected\n      }\n_H4LipBTJ\ntaskUpdateTime\n\n        key\n        uuid\n        name\n        status {\n          uuid\n          name\n          category\n        }\n        isPin\n        isSample\n        isArchive\n        statusCategory\n        assign {\n          uuid\n          name\n          avatar\n        }\n        owner {\n          uuid\n          name\n          avatar\n        }\n        createTime\n        planStartTime\n        planEndTime \n        sprintCount\n        taskCount\n        taskCountDone\n        taskCountInProgress\n        taskCountToDo\n        memberCount\n        type\n      }\n    }\n  }","variables":{"projectOrderBy":{"isPin":"DESC","namePinyin":"ASC"},"projectFilterGroup":[],"groupBy":{"projects":{"isPin":{}}},"orderBy":{"isPin":"DESC"},"filter":{"projects":{"visibleInProject_equal":true,"isArchive_equal":false}}}}'
  # gql_exp = '{"query":"{\n  buckets(groupBy: {tasks: {}}, pagination: {limit: 50, after: \"\", preciseCount: true}) {\n    tasks(filterGroup: $filterGroup, orderBy: $orderBy, includeAncestors: {pathField: \"path\"}, orderByPath: \"path\", limit: 1000) {\n      key\n      name\n      uuid\n      serverUpdateStamp\n      path\n      subTaskCount\n      subTaskDoneCount\n      position\n      status {\n        uuid\n        name\n        category\n      }\n      deadline\n      subTasks {\n        uuid\n      }\n      issueType {\n        uuid\n      }\n      subIssueType {\n        uuid\n      }\n      project {\n        uuid\n      }\n      parent {\n        uuid\n      }\n      estimatedHours\n      remainingManhour\n      importantField {\n        bgColor\n        color\n        name\n        value\n        fieldUUID\n      }\n    }\n    key\n    pageInfo {\n      count\n      totalCount\n      startPos\n      startCursor\n      endPos\n      endCursor\n      hasNextPage\n      unstable\n    }\n  }\n}\n","variables":{"groupBy":null,"orderBy":{"position":"ASC","priority":"ASC","createTime":"DESC"},"filterGroup":[],"bucketOrderBy":null}}'
  # gql_exp = '{"query":"\n    query {\n      cards (\n        filter: {\n          objectId_equal: \"RgecdGky\"\n          objectType_equal: \"project_component\"\n          status_equal: \"normal\"\n        },\n        orderBy: {  layoutY: ASC, layoutX: ASC }\n      ) {\n        key\n        uuid\n        name\n        description\n        type\n        layoutX\n        layoutY\n        layoutW\n        layoutH\n        config\n      }\n    }\n  ","variables":{}}'
  # gql_exp = '{"query":"{\n  buckets(groupBy: {tasks: {}}, pagination: {limit: 0, after: \"\", preciseCount: true}) {\n    tasks(filterGroup: $filterGroup, orderBy: $orderBy, limit: 1000, includeAncestors: {pathField: \"path\"}, orderByPath: \"path\") {\n      uuid\n    }\n    key\n    pageInfo {\n      count\n      totalCount\n      startPos\n      startCursor\n      endPos\n      endCursor\n      hasNextPage\n      unstable\n    }\n  }\n}\n","variables":{"groupBy":null,"orderBy":{"position":"ASC","createTime":"DESC"},"filterGroup":[{"project_in":["Pqmud3zhbpHjJxCm"],"issueType_in":["GwNxpqQh"]}],"bucketOrderBy":null}}'
  # gql_exp = '{"query":"{\n  buckets(groupBy: {tasks: {}}, pagination: {limit: 50, after: \"\", preciseCount: true}) {\n    tasks(filterGroup: $filterGroup, orderBy: $orderBy, includeAncestors: {pathField: \"path\"}, orderByPath: \"path\", limit: 1000) {\n      key\n      name\n      uuid\n      serverUpdateStamp\n      path\n      subTaskCount\n      subTaskDoneCount\n      position\n      status {\n        uuid\n        name\n        category\n      }\n      deadline\n      subTasks {\n        uuid\n      }\n      issueType {\n        uuid\n      }\n      subIssueType {\n        uuid\n      }\n      project {\n        uuid\n      }\n      parent {\n        uuid\n      }\n      estimatedHours\n      remainingManhour\n      importantField {\n        bgColor\n        color\n        name\n        value\n        fieldUUID\n      }\n    }\n    key\n    pageInfo {\n      count\n      totalCount\n      startPos\n      startCursor\n      endPos\n      endCursor\n      hasNextPage\n      unstable\n    }\n  }\n}\n","variables":{"groupBy":null,"orderBy":{"position":"ASC","createTime":"DESC"},"filterGroup":[{"project_in":["Pqmud3zhbpHjJxCm"],"issueType_in":["GwNxpqQh"]}],"bucketOrderBy":null}}'
  # gql_exp = '{"query":"{\n    buckets (\n      groupBy: $groupBy,\n      \n    ) {\n      key\n      product {\n        uuid\n        name\n      }\n      productModules {\n        key\n        name\n        uuid\n        position\n        path\n        updateTime\n        parent {\n          uuid\n          name\n        }\n      }\n    }\n  }","variables":{"groupBy":{"productModules":{"product":{}}}}}'
  gql_exp = '{"query":"{\n  buckets(groupBy: $groupBy, orderBy: $orderBy, filterGroup: $filterGroup, pagination: {limit: 50, after: \"\", preciseCount: true}) {\n    key\n    projects(orderBy: $projectOrderBy, filterGroup: $projectFilterGroup) {\n      _D9zH44Nb\n      _MWbAvRMb {\n        uuid\n        value\n        bgColor\n        color\n        defaultSelected\n      }\n      _2KPs1eoM {\n        uuid\n        value\n        bgColor\n        color\n        defaultSelected\n      }\n      _Jc4Y8iTU\n      _KU2TvepX\n      _PnafUbJo {\n        uuid\n        value\n        bgColor\n        color\n        defaultSelected\n      }\n      _6tZtKdar {\n        uuid\n        value\n        bgColor\n        color\n        defaultSelected\n      }\n      _GTgbdRoV {\n        uuid\n        value\n        bgColor\n        color\n        defaultSelected\n      }\n      _VquXUNwE {\n        uuid\n        value\n        bgColor\n        color\n        defaultSelected\n      }\n      _MaXoNetx {\n        uuid\n        value\n        bgColor\n        color\n        defaultSelected\n      }\n      _CLFdsCMk {\n        uuid\n        value\n        bgColor\n        color\n        defaultSelected\n      }\n      _Qd3Ekieu {\n        uuid\n        value\n        bgColor\n        color\n        defaultSelected\n      }\n      _Ru1cTVz4 {\n        avatar\n        email\n        key\n        name\n        namePinyin\n        uuid\n      }\n      _ouXT8Y7D {\n        avatar\n        email\n        key\n        name\n        namePinyin\n        uuid\n      }\n      _H4LipBTJ\n      taskUpdateTime\n      key\n      uuid\n      name\n      status {\n        uuid\n        name\n        category\n      }\n      isPin\n      isSample\n      isArchive\n      statusCategory\n      assign {\n        uuid\n        name\n        avatar\n      }\n      owner {\n        uuid\n        name\n        avatar\n      }\n      createTime\n      planStartTime\n      planEndTime\n      sprintCount\n      taskCount\n      taskCountDone\n      taskCountInProgress\n      taskCountToDo\n      memberCount\n      type\n    }\n    key\n    pageInfo {\n      count\n      totalCount\n      startPos\n      startCursor\n      endPos\n      endCursor\n      hasNextPage\n      unstable\n    }\n  }\n}\n","variables":{"projectOrderBy":{"isPin":"DESC","namePinyin":"ASC"},"projectFilterGroup":[],"groupBy":{"projects":{}},"filterGroup":[{"projects":{"visibleInProject_equal":true,"isArchive_equal":false}}]}}'
  # gql_exp = '{"query":"{\n  buckets(groupBy: $groupBy, orderBy: $orderBy, filterGroup: $filterGroup, pagination: {limit: 50, after: \"\", preciseCount: true}) {\n    key\n    projects(orderBy: $projectOrderBy, filterGroup: $projectFilterGroup) {\n      _D9zH44Nb\n      _MWbAvRMb {\n        uuid\n        value\n        bgColor\n        color\n        defaultSelected\n      }\n      _2KPs1eoM {\n        uuid\n        value\n        bgColor\n        color\n        defaultSelected\n      }\n      _Jc4Y8iTU\n      _KU2TvepX\n      _PnafUbJo {\n        uuid\n        value\n        bgColor\n        color\n        defaultSelected\n      }\n      _6tZtKdar {\n        uuid\n        value\n        bgColor\n        color\n        defaultSelected\n      }\n      _GTgbdRoV {\n        uuid\n        value\n        bgColor\n        color\n        defaultSelected\n      }\n      _VquXUNwE {\n        uuid\n        value\n        bgColor\n        color\n        defaultSelected\n      }\n      _MaXoNetx {\n        uuid\n        value\n        bgColor\n        color\n        defaultSelected\n      }\n      _CLFdsCMk {\n        uuid\n        value\n        bgColor\n        color\n        defaultSelected\n      }\n      _Qd3Ekieu {\n        uuid\n        value\n        bgColor\n        color\n        defaultSelected\n      }\n      _Ru1cTVz4 {\n        avatar\n        email\n        key\n        name\n        namePinyin\n        uuid\n      }\n      _ouXT8Y7D {\n        avatar\n        email\n        key\n        name\n        namePinyin\n        uuid\n      }\n      _H4LipBTJ\n      taskUpdateTime\n      key\n      uuid\n      name\n      status {\n        uuid\n        name\n        category\n      }\n      isPin\n      isSample\n      isArchive\n      statusCategory\n      assign {\n        uuid\n        name\n        avatar\n      }\n      owner {\n        uuid\n        name\n        avatar\n      }\n      createTime\n      planStartTime\n      planEndTime\n      sprintCount\n      taskCount\n      taskCountDone\n      taskCountInProgress\n      taskCountToDo\n      memberCount\n      type\n    }\n    key\n    pageInfo {\n      count\n      totalCount\n      startPos\n      startCursor\n      endPos\n      endCursor\n      hasNextPage\n      unstable\n    }\n  }\n}\n","variables":{"projectOrderBy":{"isPin":"DESC","namePinyin":"ASC"},"projectFilterGroup":[],"groupBy":{"projects":{}},"filterGroup":[{"projects":{"visibleInProject_equal":true,"isArchive_equal":false}}]}}'

  # TODO: fix ParseError below
  # gql_exp = '{"query":"query PRODUCTS($filter: Filter, $orderBy: OrderBy) {\n    products(filter: $filter, orderBy: $orderBy) {\n      name\n      uuid\n      key\n      owner {\n        uuid\n        name\n      }\n\n      createTime\n      assign {\n        uuid\n        name\n      }\n      \n    productComponents {\n      uuid\n      name\n      parent{\n        uuid\n      }\n      key\n      type\n      contextType\n      contextParam1\n      contextParam2\n      position\n      templateUUID\n      urlSetting{\n        url\n      }\n      views{\n        key\n        uuid\n        name\n        builtIn\n      }\n    }\n  \n      \n    }\n  }","variables":{"orderBy":{"createTime":"DESC"}}}'
  # gql_exp = '{"operationName":"LIST_TASK_GANTT_INFO","variables":{"filter":{"task_equal":"Pqmud3zhilBA7pcm"},"orderBy":{"createTime":"DESC"}},"query":"query LIST_TASK_GANTT_INFO($filter: Filter, $orderBy: OrderBy) {\n  taskGanttDatas(filter: $filter, orderBy: $orderBy) {\n    key\n    uuid\n    planStartTime\n    planEndTime\n    progress\n    task {\n      uuid\n      name\n      __typename\n    }\n    componentUUID\n    __typename\n  }\n}\n"}'
  
  ret = graphql_parser(gql_exp)
  print("---------- result ----------")
  print(ret)
