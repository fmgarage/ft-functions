## _Global.foreachInListAsValue( _list, _name )



Expression to control the **Exit Loop If** script step. You can pass a list of values into _list which is being iterated through, setting **$value** and **$i** in each iteration. If **__name** is specified, this will be used instead (e.g. for _name = "row" **$row** and **$row_i** are used).



### Parameters

#### _list

#### _name

Must be a valid variable name: [About naming fields](https://help.claris.com/en/pro-help/content/naming-fields.html).

### Result

**boolean**: the function returns *true* if **$i** exceeds the length of **_list**, otherwise *false*.



### Example

```filemaker
Set Variable [ $list ; Value: "one¶two¶three" ] 
Loop
	Exit Loop If [ _Global.foreachInListAsValue ( $list; "" ) ] 
	Show Custom Dialog [ "$value = " ; $value ] 
End Loop
```

