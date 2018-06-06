# python-parse-to-json

Parse Python code to an AST in JSON format, based upon https://github.com/m-labs/pythonparser/

Created on 2017-01-20 by Philip Guo

15-minute tutorial video: https://www.youtube.com/watch?v=wK_VVajpolI

---

Forked the HEAD of https://github.com/m-labs/pythonparser/ on 2017-01-20 into here and simplified it.

hello!

Example usage:

```
$ python parse_python_to_json.py --pp '
> def foo(a, b, *c):
>   y = a + (b - c)
>   return y
> '
{
  "body": [
    {
      "body": [
        {
          "loc": {
            "start": {
              "column": 2,
              "line": 3
            },
            "end": {
              "column": 16,
              "line": 3
            }
          },
          "_fields": [
            "targets",
            "value"
          ],
          "type": "Assign",
          "targets": [
            {
              "ctx": null,
              "loc": {
                "start": {
                  "column": 2,
                  "line": 3
                },
                "end": {
                  "column": 3,
                  "line": 3
                }
              },
              "_fields": [
                "id",
                "ctx"
              ],
              "type": "Name",
              "id": "y"
            }
          ],
          "value": {
            "loc": {
              "start": {
                "column": 6,
                "line": 3
              },
              "end": {
                "column": 16,
                "line": 3
              }
            },
            "right": {
              "loc": {
                "start": {
                  "column": 11,
                  "line": 3
                },
                "end": {
                  "column": 16,
                  "line": 3
                }
              },
              "right": {
                "ctx": null,
                "loc": {
                  "start": {
                    "column": 15,
                    "line": 3
                  },
                  "end": {
                    "column": 16,
                    "line": 3
                  }
                },
                "_fields": [
                  "id",
                  "ctx"
                ],
                "type": "Name",
                "id": "c"
              },
              "left": {
                "ctx": null,
                "loc": {
                  "start": {
                    "column": 11,
                    "line": 3
                  },
                  "end": {
                    "column": 12,
                    "line": 3
                  }
                },
                "_fields": [
                  "id",
                  "ctx"
                ],
                "type": "Name",
                "id": "b"
              },
              "_fields": [
                "left",
                "op",
                "right"
              ],
              "type": "BinOp",
              "op": {
                "loc": {
                  "start": {
                    "column": 13,
                    "line": 3
                  },
                  "end": {
                    "column": 14,
                    "line": 3
                  }
                },
                "_fields": [],
                "type": "Sub"
              }
            },
            "left": {
              "ctx": null,
              "loc": {
                "start": {
                  "column": 6,
                  "line": 3
                },
                "end": {
                  "column": 7,
                  "line": 3
                }
              },
              "_fields": [
                "id",
                "ctx"
              ],
              "type": "Name",
              "id": "a"
            },
            "_fields": [
              "left",
              "op",
              "right"
            ],
            "type": "BinOp",
            "op": {
              "loc": {
                "start": {
                  "column": 8,
                  "line": 3
                },
                "end": {
                  "column": 9,
                  "line": 3
                }
              },
              "_fields": [],
              "type": "Add"
            }
          }
        },
        {
          "loc": {
            "start": {
              "column": 2,
              "line": 4
            },
            "end": {
              "column": 10,
              "line": 4
            }
          },
          "_fields": [
            "value"
          ],
          "type": "Return",
          "value": {
            "ctx": null,
            "loc": {
              "start": {
                "column": 9,
                "line": 4
              },
              "end": {
                "column": 10,
                "line": 4
              }
            },
            "_fields": [
              "id",
              "ctx"
            ],
            "type": "Name",
            "id": "y"
          }
        }
      ],
      "loc": {
        "start": {
          "column": 0,
          "line": 2
        },
        "end": {
          "column": 10,
          "line": 4
        }
      },
      "name": "foo",
      "args": {
        "loc": {
          "start": {
            "column": 8,
            "line": 2
          },
          "end": {
            "column": 16,
            "line": 2
          }
        },
        "vararg": {
          "loc": {
            "start": {
              "column": 15,
              "line": 2
            },
            "end": {
              "column": 16,
              "line": 2
            }
          },
          "_fields": [
            "arg",
            "annotation"
          ],
          "type": "arg",
          "annotation": null,
          "arg": "c"
        },
        "args": [
          {
            "loc": {
              "start": {
                "column": 8,
                "line": 2
              },
              "end": {
                "column": 9,
                "line": 2
              }
            },
            "_fields": [
              "arg",
              "annotation"
            ],
            "type": "arg",
            "annotation": null,
            "arg": "a"
          },
          {
            "loc": {
              "start": {
                "column": 11,
                "line": 2
              },
              "end": {
                "column": 12,
                "line": 2
              }
            },
            "_fields": [
              "arg",
              "annotation"
            ],
            "type": "arg",
            "annotation": null,
            "arg": "b"
          }
        ],
        "kwarg": null,
        "defaults": [],
        "kw_defaults": [],
        "kwonlyargs": [],
        "_fields": [
          "args",
          "vararg",
          "kwonlyargs",
          "kwarg",
          "defaults",
          "kw_defaults"
        ],
        "type": "arguments"
      },
      "returns": null,
      "_fields": [
        "name",
        "args",
        "returns",
        "body",
        "decorator_list"
      ],
      "type": "FunctionDef",
      "decorator_list": []
    }
  ],
  "loc": {
    "start": {
      "column": 0,
      "line": 2
    },
    "end": {
      "column": 10,
      "line": 4
    }
  },
  "_fields": [
    "body"
  ],
  "type": "Module"
}
```
