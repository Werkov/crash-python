# -*- coding: utf-8 -*-
# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:

tasks = {}

def cache_task(task):
    tasks[int(task.task_struct['pid'])] = task

def get_task(pid):
    return tasks[pid]

def drop_task(pid):
    del tasks[pid]
