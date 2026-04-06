def post_init_hook(env):
    env['student.course']._sync_batch_course_menus()
