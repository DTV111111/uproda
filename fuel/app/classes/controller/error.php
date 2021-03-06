<?php
class Controller_Error extends \Controller_Rest
{
	protected $default_format = 'json';

	public function before()
	{
		parent::before();
		Libs_Config::load();
		Libs_Lang::load();

		if (! \Input::is_ajax()) {
			$this->theme = \Theme::instance();
			$this->theme->active('skeleton');
			$this->theme->asset->add_path('assets/global', ['css', 'js', 'img']);
			$template = $this->theme->set_template('template');
			$this->theme->set_partial('head', $this->theme->presenter('head'), 'view', true);
			$this->theme->set_partial('header', $this->theme->presenter('error/header'), 'view', true);
			$this->theme->set_partial('footer', $this->theme->presenter('footer'), 'view', true );
			$this->theme->set_partial('form', null);
		}
	}

	public function action_index($page = 1)
	{
		throw new HttpNotFoundException();
	}

	public function action_400()
	{
		$this->response_status = 400;
		if (\Input::is_ajax())
		{
			return $this->response([
				'error'  => 'Bad Request',
				'status' => 400,
			], 400);
		}
		else
		{
			$this->theme->set_partial('content', 'error/content')->set([
				'error'  => $this->theme->presenter('error/400'),
			]);
		}
	}

	public function action_403()
	{
		$this->response_status = 403;
		if (\Input::is_ajax())
		{
			return $this->response([
				'error'  => 'Access Forbidden',
				'status' => 403,
			], 403);
		}
		else
		{
			$this->theme->set_partial('content', 'error/content')->set([
				'error'  => $this->theme->presenter('error/403'),
			]);
		}
	}

	public function action_404()
	{
		$this->response_status = 404;
		if (\Input::is_ajax())
		{
			return $this->response([
				'error'  => 'Page Not Found',
				'status' => 404,
			], 404);
		}
		else
		{
			$this->theme->set_partial('content', 'error/content')->set([
				'error'  => $this->theme->presenter('error/404'),
			]);
		}
	}

	public function action_500()
	{
		$this->response_status = 500;
		if (\Input::is_ajax())
		{
			return $this->response([
				'error'  => 'Internal Server Error',
				'status' => 500,
			], 500);
		}
		else
		{
			$this->theme->set_partial('content', 'error/content')->set([
				'error'  => $this->theme->presenter('error/500'),
			]);
		}
	}

	public function after($response)
	{
		if (empty($response) or ! $response instanceof Response)
		{
			$response = \Response::forge($this->theme->render());
		}

		$response->set_status($this->response_status);
		return parent::after($response);
	}
}
