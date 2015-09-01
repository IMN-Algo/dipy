# -*- coding:utf-8 -*-

import vtk


class InteractorStyleImageAndTrackballActor(vtk.vtkInteractorStyleUser):
    """ Interactive manipulation of the camera specialized for images that can
    also manipulates objects in the scene independent of each other.

    This interactor style allows the user to interactively manipulate (pan and
    zoom) the camera. It also allows the user to interact (rotate, pan, etc.)
    with objects in the scene independent of each other. It is specially
    designed to work with a grid of actors.

    Several events are overloaded from its superclass `vtkInteractorStyle`,
    hence the mouse bindings are different. (The bindings keep the camera's
    view plane normal perpendicular to the x-y plane.)

    In summary the mouse events for this interaction style are as follows:
    - Left mouse button: rotates the selected object around its center point
    - Ctrl + left mouse button: spins the selected object around its view plane normal
    - Shift + left mouse button: pans the selected object
    - Middle mouse button: pans the camera
    - Right mouse button: dollys the camera
    - Mouse wheel: dollys the camera

    """
    def __init__(self):
        self.trackball_interactor_style = vtk.vtkInteractorStyleTrackballActor()
        self.image_interactor_style = vtk.vtkInteractorStyleImage()

    def on_left_button_pressed(self, obj, evt):
        self.trackball_interactor_style.OnLeftButtonDown()

    def on_left_button_released(self, obj, evt):
        self.trackball_interactor_style.OnLeftButtonUp()

    def on_right_button_pressed(self, obj, evt):
        self.image_interactor_style.OnRightButtonDown()

    def on_right_button_released(self, obj, evt):
        self.image_interactor_style.OnRightButtonUp()

    def on_middle_button_pressed(self, obj, evt):
        self.image_interactor_style.OnMiddleButtonDown()

    def on_middle_button_released(self, obj, evt):
        self.image_interactor_style.OnMiddleButtonUp()

    def on_mouse_moved(self, obj, evt):
        self.trackball_interactor_style.OnMouseMove()
        self.image_interactor_style.OnMouseMove()

    def on_mouse_wheel_forward(self, obj, evt):
        self.image_interactor_style.OnMouseWheelForward()

    def on_mouse_wheel_backward(self, obj, evt):
        self.image_interactor_style.OnMouseWheelBackward()

    def SetInteractor(self, interactor):
        # Internally these `InteractorStyle` objects need an handle to a
        # `vtkWindowInteractor` object and this is done via `SetInteractor`.
        # However, this has a the side effect of adding directly their
        # observers to `interactor`!
        self.trackball_interactor_style.SetInteractor(interactor)
        self.image_interactor_style.SetInteractor(interactor)

        # Remove all observers previously set. Those were *most likely* set by
        # `vtkInteractorStyleTrackballActor` and `vtkInteractorStyleImage`.
        #
        # Note: Be sure that no observer has been manually added to the
        #       `interactor` before setting the InteractorStyle.
        interactor.RemoveAllObservers()

        # This class is a `vtkClass` (instead of `object`), so `super()` cannot be used.
        # Also the method `SetInteractor` is not overridden by `vtkInteractorStyleUser`
        # so we have to call directly the one from `vtkInteractorStyle`.
        # In addition to setting the interactor, the following line
        # adds the necessary hooks to listen to this instance's observers.
        vtk.vtkInteractorStyle.SetInteractor(self, interactor)

        self.AddObserver("LeftButtonPressEvent", self.on_left_button_pressed)
        self.AddObserver("LeftButtonReleaseEvent", self.on_left_button_released)
        self.AddObserver("RightButtonPressEvent", self.on_right_button_pressed)
        self.AddObserver("RightButtonReleaseEvent", self.on_right_button_released)
        self.AddObserver("MiddleButtonPressEvent", self.on_middle_button_pressed)
        self.AddObserver("MiddleButtonReleaseEvent", self.on_middle_button_released)
        self.AddObserver("MouseMoveEvent", self.on_mouse_moved)

        # These observers need to be added directly to the interactor because
        # `vtkInteractorStyleUser` does not forward these events.
        interactor.AddObserver("MouseWheelForwardEvent", self.on_mouse_wheel_forward)
        interactor.AddObserver("MouseWheelBackwardEvent", self.on_mouse_wheel_backward)
