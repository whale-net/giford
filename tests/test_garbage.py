from giford.image import MultiImage
from giford.frame.frame_batch import FrameBatch
from giford.action.reshape import Reshape, ReshapeMethod


def test_feed_garbage_to_multi_image(
    temp_output_gif: str, orange_swirl_batch: FrameBatch
):
    # this test should fail
    try:
        new_batch = FrameBatch()
        for i, frame in enumerate(orange_swirl_batch.frames):
            new_batch.add_frame(frame)

            if (i % 3) == 0:
                r = Reshape()
                temp_batch = FrameBatch()
                temp_batch.add_frame(frame).add_frame(frame).add_frame(frame).add_frame(
                    frame
                )
                # this should be smaller probably but idk what is going on
                temp_batch = r.process(temp_batch, ReshapeMethod.RESCALE, 0.25)
                new_batch.add_batch(temp_batch)

        mimg = MultiImage.create_from_frame_batch(new_batch)
        mimg.save(temp_output_gif)
    except ValueError as ve:
        assert "iterator too short: " in str(ve)
        pass
    except:
        assert False
